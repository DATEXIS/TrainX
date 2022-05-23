import json
import logging
import os
import tempfile
from typing import List

import flair
import torch
from flair.data import Corpus, Sentence
from flair.datasets import ColumnCorpus
from flair.embeddings import StackedEmbeddings, FlairEmbeddings, WordEmbeddings
from flair.models import SequenceTagger
from model import B64TarWrapper
from texoopy import Dataset, Document, Annotation, MentionAnnotation
from tqdm import tqdm

logger = logging.getLogger('__name__')


def teXooDocument2FlairBIOESSentence(document: Document, apply_sentence_split: bool = False,
                                     allowed_sources: List[str] = ['USER', 'SILVER', 'GOLD']) -> Sentence:
    if apply_sentence_split:
        raise NotImplemented()  # TODO implement me

    flair_sentence: Sentence = Sentence(document.text, use_tokenizer=True)
    for token in flair_sentence.tokens:
        token.add_tag('BIOES', 'O-ENT')
    annotation: Annotation
    for ann in document.annotations:
        if ann.source not in allowed_sources:
            continue
        begin = ann.begin
        end = ann.begin + ann.length
        tokens = list()
        for token in flair_sentence.tokens:
            if token.start_pos >= begin and token.end_pos <= end:
                tokens.append(token)
        if len(tokens) == 1:
            if tokens[0].get_tag('BIOES').value != 'O-ENT':
                continue
            tokens[0].add_tag('BIOES', 'S-ENT')
        elif len(tokens) > 1:
            # just make sure that tokens are sorted properly
            tokens = sorted(tokens, key=lambda tok: tok.start_pos)
            existing_tags = set([tok.get_tag('BIOES').value for tok in tokens])
            if existing_tags != {'O-ENT'}:
                # Some tokens are already tagged, skip annotation
                continue
            for tok in tokens:
                tok.add_tag('BIOES', 'I-ENT')
            tokens[0].add_tag('BIOES', 'B-ENT')
            tokens[-1].add_tag('BIOES', 'E-ENT')
    return flair_sentence


def teXoo2CoNLLFile(path_to_json: str, allowed_sources: List[str]) -> '_TemporaryFileWrapper':
    """
    Reads a TeXoo JSON, generates a temporary CoNLL-style NER training file
    :param allowed_sources:
    :param path_to_json:
    :return:
    """
    def document_does_not_contain_trainable_annotations(document: Document, allowed_sources: List[str]):
        for annotation in document.annotations:
            if annotation.source in allowed_sources:
                return False
        return True

    with open(path_to_json, 'r') as f:
        dataset: Dataset = Dataset.from_json(json.load(f))
    document: Document
    f = tempfile.NamedTemporaryFile()
    for document in tqdm(dataset.documents, desc='Preprocessing {} for NER training'.format(path_to_json)):
        if document_does_not_contain_trainable_annotations(document, allowed_sources):  # TODO this should be optional
            continue
        flair_sentence = teXooDocument2FlairBIOESSentence(document, allowed_sources=allowed_sources)
        for token in flair_sentence.tokens:
            line: str = '{} \t {}\n'.format(token.text, token.get_tag('BIOES').value)
            f.write(line.encode('utf-8'))
        f.write(b'\n')
    f.flush()
    logger.info('Parsed TeXoo dataset {} to temporary CoNLL file {}'.format(path_to_json, f.name))
    return f


class NER:
    def __init__(self, model_base_path: str, device: str = 'cpu', max_epochs: int = 150):
        """
        Initialises an abstraction layer over the Flair SequenceTagger
        :param device:
        :param model_base_path: Path to model base folder
        """
        self.device = device
        self.is_trained: bool = False
        self.model_base_path = model_base_path
        self.max_epochs = max_epochs
        flair.device = torch.device(device)
        try:
            self.ner: SequenceTagger = SequenceTagger.load(os.path.join(self.model_base_path, 'best-model.pt'))
            self.is_trained = False
        except FileNotFoundError:
            logger.info('No NER model found, needs to be trained.')

    @classmethod
    def from_tar(cls, model_tar: B64TarWrapper, device: str, max_epochs: int = 150) -> 'NER':
        path = model_tar.get_extract()
        return cls(model_base_path=path, device=device, max_epochs=max_epochs)

    def to_tar(self) -> B64TarWrapper:
        """
        Triggers the storage of both encoders and wraps them into a B64TarWrapper
        :return: tar-ed statedicts for both encoders
        """
        return B64TarWrapper.from_files(paths=[os.path.join(self.model_base_path, 'best-model.pt')])

    def train(self, train_texoo_path: str):
        """
        :param train_texoo_path: Path to train TeXoo file
        :param test_texoo: Path to test TeXoo file
        :param dev_texoo: Path to dev TeXoo file
        :return: 
        """
        if self.is_trained:
            logger.warning('Re-training a previously trained model...')
        # TODO this will fail in a strange way when the dataset is empty
        with teXoo2CoNLLFile(train_texoo_path, allowed_sources=['USER', 'GOLD', 'SILVER']) as f_train:
            corpus: Corpus = ColumnCorpus(
                '.',
                {0: 'text', 1: 'BIOES'},
                train_file=f_train.name,
                dev_file=f_train.name,
                test_file=f_train.name  # TODO if this is None then it takes samples from train for some reason
            )  # TODO we need to find a way without a test file, otherwise it will perform a full test afterwards

        tag_type = 'BIOES'
        tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
        embedding_types = [
            WordEmbeddings('glove'),
            FlairEmbeddings('news-forward'),
            FlairEmbeddings('news-backward'),
        ]
        embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)
        from flair.models import SequenceTagger
        self.ner: SequenceTagger = SequenceTagger(hidden_size=256,
                                                  embeddings=embeddings,
                                                  tag_dictionary=tag_dictionary,
                                                  tag_type=tag_type)
        from flair.trainers import ModelTrainer
        trainer: ModelTrainer = ModelTrainer(self.ner, corpus)
        trainer.train(base_path=self.model_base_path,
                      learning_rate=0.1,
                      mini_batch_size=128,
                      max_epochs=self.max_epochs,
                      embeddings_storage_mode=self.device)
        self.is_trained = True

    def predict(self, dataset: Dataset) -> None:
        """
        Applies NER model onto the given dataset and creates MentionAnnotations of type PREDICT with confidence score.
        :param dataset:
        :return:
        """
        for doc in tqdm(dataset.documents, desc='Applying pre-trained NER model'):
            flair_doc = Sentence(doc.text)
            self.ner.predict(flair_doc)
            for entity in flair_doc.get_spans('BIOES'):
                doc.annotations.append(MentionAnnotation(
                    begin=entity.start_pos,
                    length=entity.end_pos - entity.start_pos,
                    text=entity.text,
                    source='PRED',
                    confidence=entity.score
                ))
