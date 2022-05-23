import logging
import os
import tempfile
from typing import List, Tuple, Union, Dict

import torch
from biencodernel.knn import FaissHNSWIndex, FaissExactKNNIndex
from model import B64TarWrapper
from texoopy import Dataset, MentionAnnotation, NamedEntityAnnotation
from torch import nn, Tensor
from torch.optim import Adam
from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import BertTokenizer, get_linear_schedule_with_warmup, BertModel

logger = logging.getLogger(__name__)


class Encoder(nn.Module):

    def __init__(self, tokenizer: BertTokenizer, freeze_embeddings: bool = True, bert_model: str = 'bert-base-uncased'):
        """
        :param tokenizer: The tokenizer that was used to generate the token ids (Necessary for resizing the vocab of the model)
        :param pooling: CLS (CLS token) or AVG
        :param freeze_embeddings: freeze embedding layer as suggested by Hummeau et al. 2019
        :param bert_model: Identifier of the pre-trained huggingface bert model
        """

        super(Encoder, self).__init__()
        self.bert = BertModel.from_pretrained(bert_model)
        if freeze_embeddings:
            for param in list(self.bert.embeddings.parameters()):
                param.requires_grad = False
        self.bert.resize_token_embeddings(len(tokenizer))

    def forward(self, token_ids: Tensor) -> Tensor:
        hidden_states, cls_tokens = self.bert(token_ids)
        return cls_tokens


class CrossEntropyLoss:

    def __init__(self, device: str = 'cpu', reduction: str = 'mean'):
        """
        Cross Entropy Loss as mentioned in Humeau et al. 2019 - Poly Encoders
        :param device: cpu | cuda
        """
        logger.info('Initializing CrossEntropyLoss on device {} with reduction {}.'.format(device, reduction))
        self.device = device
        self.loss_func = torch.nn.CrossEntropyLoss(reduction=reduction).to(self.device)

    def loss(self, mention_vecs: torch.Tensor, concept_vecs: torch.Tensor) -> torch.Tensor:
        assert concept_vecs.size() == mention_vecs.size()
        dot_products = torch.matmul(mention_vecs, concept_vecs.t()).to(self.device)
        y_target = torch.arange(0, concept_vecs.shape[0]).to(self.device)
        return self.loss_func(dot_products, y_target)

    def __call__(self, mention_vecs: torch.Tensor, concept_vecs: torch.Tensor) -> torch.Tensor:
        return self.loss(mention_vecs=mention_vecs, concept_vecs=concept_vecs)


class BiEncoder:

    def __init__(self, device: str, tokenizer: BertTokenizer, bert_model: str = 'bert-base-uncased'):
        logger.info("Initializing BiEncoder on device {}".format(device))
        self.device: str = device
        self.tokenizer: BertTokenizer = tokenizer
        self.encoder_mention: Encoder = Encoder(tokenizer=self.tokenizer, bert_model=bert_model).to(self.device)
        self.encoder_concept: Encoder = Encoder(tokenizer=self.tokenizer, bert_model=bert_model).to(self.device)
        self.loss_func = CrossEntropyLoss(self.device)

    @classmethod
    def from_pretrained(cls, tokenizer: BertTokenizer, mention_encoder_path: str, concept_encoder_path: str,
                        device: str) -> 'BiEncoder':
        biencoder = cls(device=device, tokenizer=tokenizer)
        biencoder.encoder_mention.load_state_dict(torch.load(mention_encoder_path, map_location=device))
        biencoder.encoder_concept.load_state_dict(torch.load(concept_encoder_path, map_location=device))
        return biencoder

    @classmethod
    def from_tar(cls, model_tar: B64TarWrapper, tokenizer: BertTokenizer, device: str) -> 'BiEncoder':
        path = model_tar.get_extract()
        mention_encoder_path = os.path.join(path, 'encoder_mention.statedict')
        concept_encoder_path = os.path.join(path, 'encoder_concept.statedict')
        return BiEncoder.from_pretrained(tokenizer=tokenizer, mention_encoder_path=mention_encoder_path,
                                         concept_encoder_path=concept_encoder_path, device=device)

    def to_tar(self) -> B64TarWrapper:
        """
        Triggers the storage of both encoders and wraps them into a B64TarWrapper
        :return: tar-ed statedicts for both encoders
        """
        temp_dir = tempfile.mkdtemp()
        self.save_encoders(temp_dir)
        return B64TarWrapper.from_files(
            paths=[
                os.path.join(temp_dir, 'encoder_mention.statedict'),
                os.path.join(temp_dir, 'encoder_concept.statedict')
            ]
        )

    def train(self, train_dataloader: DataLoader, learning_rate: float, epochs: int, warmup_steps: int, clip_grad_norm: bool):
        optimizer_mention = Adam(self.encoder_mention.parameters(), lr=learning_rate)
        optimizer_concept = Adam(self.encoder_concept.parameters(), lr=learning_rate)
        scheduler_mention = get_linear_schedule_with_warmup(optimizer_mention,
                                                            num_warmup_steps=warmup_steps,
                                                            num_training_steps=len(train_dataloader) * epochs)
        scheduler_concept = get_linear_schedule_with_warmup(optimizer_concept,
                                                            num_warmup_steps=warmup_steps,
                                                            num_training_steps=len(train_dataloader) * epochs)

        for epoch_num in tqdm(range(epochs), desc='Epoch'):
            self.__train_loop(
                dataloader=train_dataloader,
                optimizer_mention=optimizer_mention,
                scheduler_mention=scheduler_mention,
                optimizer_concept=optimizer_concept,
                scheduler_concept=scheduler_concept,
                clip_grad_norm=clip_grad_norm
            )

    def __train_loop(
            self,
            dataloader: DataLoader,
            optimizer_mention: Optimizer,
            scheduler_mention,
            optimizer_concept: Optimizer,
            scheduler_concept,
            clip_grad_norm: bool,
    ) -> List[float]:
        """
        Performs a training of both encoders and returns the train loss.
        :param dataloader:
        :param optimizer_mention:
        :param optimizer_concept:
        :return: minibatch losses
        """
        self.encoder_mention.train()
        self.encoder_concept.train()
        minibatch_losses = []
        for step_num, batch_data in tqdm(enumerate(dataloader), desc='Training', total=len(dataloader)):
            mention_tokens, concept_tokens, _ = batch_data
            mention_tokens = mention_tokens.to(self.device)
            concept_tokens = concept_tokens.to(self.device)
            vecs_mention = self.encoder_mention(mention_tokens)
            vecs_concept = self.encoder_concept(concept_tokens)
            batch_loss = self.loss_func(vecs_mention, vecs_concept)
            minibatch_losses.append(batch_loss.item())
            self.encoder_mention.zero_grad()
            self.encoder_concept.zero_grad()
            if clip_grad_norm:
                torch.nn.utils.clip_grad_norm_(self.encoder_mention.parameters(), 1.0)
                torch.nn.utils.clip_grad_norm_(self.encoder_concept.parameters(), 1.0)
            batch_loss.backward()
            optimizer_mention.step()
            optimizer_concept.step()
            scheduler_mention.step()
            scheduler_concept.step()
        return minibatch_losses

    def predict(self, prediction_dataloader: DataLoader, prediction_dataset: Dataset, kb_dataloader: DataLoader, omp_num_threads: int = 1, use_exact_knn: bool = True) -> None:
        """
        Applies NEL model onto all MentionAnnotations and transforms them into NamedEntityAnnotations with confidence
        :param dataset:
        :return:
        """
        with torch.no_grad():
            self.encoder_mention.eval()
            self.encoder_concept.eval()

            kb_embeddings_cache = dict()
            for step_num, batch_data in tqdm(enumerate(kb_dataloader), desc='Generating KB candidate embeddings',
                                             total=len(kb_dataloader)):
                concept_ids, concept_tokens = batch_data
                concept_tokens = concept_tokens.to(self.device)
                concept_embeddings = self.encoder_concept(concept_tokens)
                for kb_id, concept_embedding in zip(concept_ids, concept_embeddings):
                    kb_embeddings_cache[kb_id] = concept_embedding.to('cpu')

            # TODO make configurable and switchable between exact kNN and HNSW
            if use_exact_knn:
                knn_index = FaissExactKNNIndex(kb_embeddings_cache, omp_num_threads=omp_num_threads)
            else:
                knn_index = FaissHNSWIndex(kb_embeddings_cache, m=16, efSearch=100, efConstruction=100, omp_num_threads=omp_num_threads)
            del kb_embeddings_cache

            predictions: Dict[int, Dict[str, Union[str, float]]] = dict()

            for step_num, batch_data in tqdm(enumerate(prediction_dataloader), desc='NEL prediction',
                                             total=len(prediction_dataloader)):

                mention_tokens, annotation_ids = batch_data
                mention_tokens = mention_tokens.to(self.device)
                mention_embeddings = self.encoder_mention(mention_tokens)

                for mention_embedding, annotation_id in zip(mention_embeddings.to('cpu'), annotation_ids):
                    annotation_id = annotation_id.item()
                    knn_ids, distances = zip(*knn_index.get_knn_ids_for_vector(mention_embedding, k=2))
                    confidence = max(distances[1] - distances[0], 0)
                    predictions[annotation_id] = {'refId': knn_ids[0], 'confidence': confidence}

            for doc in prediction_dataset.documents:
                new_annotations: List[NamedEntityAnnotation] = list()
                old_annotations: List[MentionAnnotation] = list()
                for ann in doc.annotations:
                    if ann.uid in predictions.keys() and type(ann) is MentionAnnotation:
                        new_annotations.append(NamedEntityAnnotation(
                            uid=ann.uid,
                            begin=ann.begin,
                            length=ann.length,
                            text=ann.text,
                            source='PRED',
                            refId=predictions[ann.uid]['refId'],
                            confidence=ann.confidence + predictions[ann.uid]['confidence'],
                        ))
                        old_annotations.append(ann)
                for ann in old_annotations:
                    doc.annotations.remove(ann)
                doc.annotations += new_annotations


    def save_encoders(self, path, model_identifier: str = '') -> Tuple[str, str]:
        """
        Saves encoders and returns the paths.
        :param path: base path
        :param model_identifier: unique identifier to separate paths
        :return: paths of the mention encoder and concept encoder statedicts
        """
        # TODO the tokenizers should be saved as well in this directory
        path = os.path.join(path, model_identifier)
        os.makedirs(path, exist_ok=True)
        mention_encoder_path = os.path.join(path, 'encoder_mention.statedict')
        concept_encoder_path = os.path.join(path, 'encoder_concept.statedict')
        torch.save(self.encoder_mention.state_dict(), mention_encoder_path)
        torch.save(self.encoder_concept.state_dict(), concept_encoder_path)
        return mention_encoder_path, concept_encoder_path
