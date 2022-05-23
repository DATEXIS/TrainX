import logging
import os
import tempfile
from typing import List, Union

import ray
import requests
from torch.utils.data import DataLoader, RandomSampler

from biencodernel.biencoder import BiEncoder
from biencodernel.datasets import MentionDataset, KBDataset, NELPredictDataset
from biencodernel.ner import NER
from biencodernel.utils import get_gpu_ids
from model import JobContainer, JobStatus, B64TarWrapper, MLModel

logger = logging.getLogger(__name__)

gpu_ids = get_gpu_ids()


@ray.remote
class TrainJob:
    def __init__(self, job_container):
        self.job_container = job_container
        self.job_container.mljob.status = JobStatus.QUEUED

    def get_status(self) -> JobStatus:
        return self.job_container.mljob.status

    def train(self, config, kb_dataset: KBDataset, gpu_ids: List[Union[None, str]] = []):
        self.job_container.mljob.status = JobStatus.RUNNING
        if len(gpu_ids) == 0:  # NO GPU, train parallel on CPU
            ner = _NERTrainJobCPU.remote(job_container=self.job_container, retrain=config['retrain_ner'],
                                         max_epochs=config['ner_max_epochs'])
            nel = _NELTrainJobCPU.remote(
                job_container=self.job_container,
                batch_size=config['batch_size'],
                max_length=config['input_length'],
                kb_dataset=kb_dataset,
                learning_rate=config['learning_rate'],
                epochs=config['epochs'],
                warmup_steps=config['warmup_steps'],
                retrain=config['retrain_ner'],
                clip_grad_norm=config['clip_grad_norm'],
                bert_model=config['bert_model']
            )
            ner_future = ner.get_model.remote()
            nel_future = nel.get_model.remote()
            model = ray.get(ner_future) + ',' + ray.get(nel_future)

        elif len(gpu_ids) == 1:  # one GPU, train sequentially on GPU
            ner = _NERTrainJobGPU.remote(job_container=self.job_container, retrain=config['retrain_ner'],
                                         max_epochs=config['ner_max_epochs'])
            ner_model: str = ray.get(ner.get_model.remote())
            ray.kill(ner)
            nel = _NELTrainJobGPU.remote(
                job_container=self.job_container,
                batch_size=config['batch_size'],
                max_length=config['input_length'],
                kb_dataset=kb_dataset,
                learning_rate=config['learning_rate'],
                epochs=config['epochs'],
                warmup_steps=config['warmup_steps'],
                retrain=config['retrain_ner'],
                clip_grad_norm=config['clip_grad_norm'],
                bert_model=config['bert_model']
            )
            nel_model: str = ray.get(nel.get_model.remote())
            ray.kill(nel)
            model = ner_model + ',' + nel_model

        elif len(gpu_ids) > 1:  # more than one GPU, take two and train in parallel
            ner = _NERTrainJobGPU.remote(job_container=self.job_container, retrain=config['retrain_ner'])
            nel = _NELTrainJobGPU.remote(
                job_container=self.job_container,
                batch_size=config['batch_size'],
                max_length=config['input_length'],
                kb_dataset=kb_dataset,
                learning_rate=config['learning_rate'],
                epochs=config['epochs'],
                warmup_steps=config['warmup_steps'],
                retrain=config['retrain_ner'],
                clip_grad_norm=config['clip_grad_norm'],
                bert_model=config['bert_model']
            )
            ner_future = ner.get_model.remote()
            nel_future = nel.get_model.remote()
            model = ray.get(ner_future) + ',' + ray.get(nel_future)

        self.job_container.mljob.status = JobStatus.FINISHED
        self.job_container.mljob.dataset = None
        self.post_finished_train_job_back_to_callback_url(model)
        ray.actor.exit_actor()

    def post_finished_train_job_back_to_callback_url(self, model: str):
        self.job_container.mljob.model = MLModel(binary=model)
        try:
            resp = requests.post(self.job_container.callbackUrl, json=self.job_container.to_json(), timeout=300)
            return resp.status_code
        except requests.Timeout as e:
            logger.error('Got timeout while trying to post results of train job:', e)


@ray.remote(num_gpus=1)
class _NERTrainJobGPU:
    logger = logging.getLogger(__name__)

    def __init__(self, job_container: JobContainer, gpu_id: str = 'cuda:0', retrain: bool = False,
                 max_epochs: int = 150):

        if not job_container.mljob.model and retrain:
            logger.info("No NER model received, will train a new one.")
            self.ner: NER = NER(model_base_path=tempfile.mkdtemp(), device=gpu_id, max_epochs=max_epochs)
        else:
            logger.info("NER model received, will continue training.")
            ner_model_base64 = job_container.mljob.model.binary.split(',')[0]
            self.ner = NER.from_tar(B64TarWrapper('ner', ner_model_base64), device=gpu_id, max_epochs=max_epochs)
        temp_texoo_path = os.path.join(tempfile.mkdtemp(), 'tmp_texoo_ner_train.json')
        with open(temp_texoo_path, 'w') as f:
            f.write(job_container.mljob.dataset.to_json())
        self.ner.train(temp_texoo_path)

    def get_model(self) -> str:
        return self.ner.to_tar().get_base64_str()


@ray.remote
class _NERTrainJobCPU:
    logger = logging.getLogger(__name__)

    def __init__(self, job_container: JobContainer, retrain: bool = False, max_epochs: int = 150):

        if not job_container.mljob.model and retrain:
            logger.info("No NER model received, will train a new one.")
            self.ner: NER = NER(model_base_path=tempfile.mkdtemp(), device='cpu', max_epochs=max_epochs)
        else:
            logger.info("NER model received, will continue training.")
            ner_model_base64 = job_container.mljob.model.binary.split(',')[0]
            self.ner = NER.from_tar(B64TarWrapper('ner', ner_model_base64), device='cpu', max_epochs=max_epochs)
        temp_texoo_path = os.path.join(tempfile.mkdtemp(), 'tmp_texoo_ner_train.json')
        with open(temp_texoo_path, 'w') as f:
            f.write(job_container.mljob.dataset.to_json())
        self.ner.train(temp_texoo_path)

    def get_model(self) -> str:
        return self.ner.to_tar().get_base64_str()


@ray.remote(num_gpus=1)
class _NELTrainJobGPU:
    def __init__(self, job_container: JobContainer, batch_size: int, max_length: int, kb_dataset: KBDataset,
                 learning_rate: float, epochs: int, bert_model: str, warmup_steps: int = 0,
                 retrain: bool = False, gpu_id: str = 'cuda:0', clip_grad_norm: bool = False,
                 ):

        temp_texoo_path = os.path.join(tempfile.mkdtemp(), 'tmp_texoo_ner_train.json')
        with open(temp_texoo_path, 'w') as f:
            f.write(job_container.mljob.dataset.to_json())
        train_ds = MentionDataset(
            path_to_json=temp_texoo_path,
            max_length=max_length,
            kb_dataset=kb_dataset,
            allowed_sources=['GOLD', 'USER', 'SILVER', 'TRAIN'],
            bert_model=bert_model
        )

        if not job_container.mljob.model or not retrain:
            logger.info("No NEL model received, will train a new one.")
            self.nel = BiEncoder(device=gpu_id, tokenizer=train_ds.tokenizer, bert_model=bert_model)
        else:
            logger.info("NEL model received, will continue training.")
            nel_model_base64 = job_container.mljob.model.binary.split(',')[1]
            self.nel = BiEncoder.from_tar(B64TarWrapper('nel', nel_model_base64), tokenizer=train_ds.tokenizer,
                                          device=gpu_id)

        if len(train_ds) != 0:
            train_dl = DataLoader(dataset=train_ds, sampler=RandomSampler(train_ds), batch_size=batch_size,
                                  drop_last=False, pin_memory=True)

            self.nel.train(train_dataloader=train_dl, learning_rate=learning_rate, epochs=epochs,
                           warmup_steps=warmup_steps, clip_grad_norm=clip_grad_norm)
        else:
            logger.warning("NEL train job received no suitable training data, skipping training.")

    def get_model(self) -> str:
        return self.nel.to_tar().get_base64_str()


@ray.remote
class _NELTrainJobCPU:
    def __init__(self, job_container: JobContainer, batch_size: int, max_length: int, kb_dataset: KBDataset,
                 learning_rate: float, epochs: int, bert_model: str, warmup_steps: int = 0, retrain: bool = False,
                 clip_grad_norm: bool = False):

        temp_texoo_path = os.path.join(tempfile.mkdtemp(), 'tmp_texoo_ner_train.json')
        with open(temp_texoo_path, 'w') as f:
            f.write(job_container.mljob.dataset.to_json())
        train_ds = MentionDataset(
            path_to_json=temp_texoo_path,
            max_length=max_length,
            kb_dataset=kb_dataset,
            allowed_sources=['GOLD', 'USER', 'SILVER', 'TRAIN'],
            bert_model=bert_model
        )

        if not job_container.mljob.model or not retrain:
            logger.info("No NEL model received, will train a new one.")
            self.nel = BiEncoder(device='cpu', tokenizer=train_ds.tokenizer, bert_model=bert_model)
        else:
            logger.info("NEL model received, will continue training.")
            nel_model_base64 = job_container.mljob.model.binary.split(',')[1]
            self.nel = BiEncoder.from_tar(B64TarWrapper('nel', nel_model_base64), tokenizer=train_ds.tokenizer,
                                          device='cpu')

        if len(train_ds) != 0:
            train_dl = DataLoader(dataset=train_ds, sampler=RandomSampler(train_ds), batch_size=batch_size,
                                  drop_last=False, pin_memory=True)

            self.nel.train(train_dataloader=train_dl, learning_rate=learning_rate, epochs=epochs,
                           warmup_steps=warmup_steps, clip_grad_norm=clip_grad_norm)
        else:
            logger.warning("NEL train job received no suitable training data, skipping training.")

    def get_model(self) -> str:
        return self.nel.to_tar().get_base64_str()


@ray.remote
class PredictJob:
    def __init__(self, job_container: JobContainer):
        self.job_container = job_container
        self.job_container.mljob.status = JobStatus.QUEUED

    def get_status(self) -> JobStatus:
        return self.job_container.mljob.status

    def predict(self, config, kb_dataset: KBDataset, gpu_ids: List[Union[None, str]] = []):
        self.job_container.mljob.status = JobStatus.RUNNING
        dataset = self.job_container.mljob.dataset

        for doc in dataset.documents:
            doc.annotations = [ann for ann in doc.annotations if ann.source != 'PRED']  # remove old PRED annotations

        kb_dl = DataLoader(dataset=kb_dataset, batch_size=config['batch_size'], drop_last=False, pin_memory=True)

        ner_model_base64, nel_model_base64 = self.job_container.mljob.model.binary.split(',')

        if len(gpu_ids) == 0:
            ner = NER.from_tar(B64TarWrapper('ner', ner_model_base64), device='cpu')
            ner.predict(dataset=dataset)
            nel_ds = NELPredictDataset(dataset=dataset, max_length=config['input_length'], allowed_ner_sources=['PRED'],
                                       bert_model=config['bert_model'])
            nel_dl = DataLoader(dataset=nel_ds, batch_size=config['batch_size'], drop_last=False, pin_memory=True)
            nel = BiEncoder.from_tar(B64TarWrapper('nel', nel_model_base64), tokenizer=nel_ds.tokenizer, device='cpu')
            nel.predict(prediction_dataloader=nel_dl, prediction_dataset=dataset, kb_dataloader=kb_dl)

        if len(gpu_ids) > 0:
            ner = NER.from_tar(B64TarWrapper('ner', ner_model_base64), device='cuda:0')
            ner.predict(dataset=dataset)
            nel_ds = NELPredictDataset(dataset=dataset, max_length=config['input_length'], allowed_ner_sources=['PRED'],
                                       bert_model=config['bert_model'])
            nel_dl = DataLoader(dataset=nel_ds, batch_size=config['batch_size'], drop_last=False, pin_memory=True)
            nel = BiEncoder.from_tar(B64TarWrapper('nel', nel_model_base64), tokenizer=nel_ds.tokenizer,
                                     device='cuda:0')
            nel.predict(prediction_dataloader=nel_dl, prediction_dataset=dataset, kb_dataloader=kb_dl)

        self.post_finished_predict_job_to_callback_url()
        ray.actor.exit_actor()

    def post_finished_predict_job_to_callback_url(self):
        self.job_container.mljob.model = None  # Remove model
        self.job_container.mljob.status = JobStatus.FINISHED
        try:
            resp = requests.post(self.job_container.callbackUrl, json=self.job_container.to_json(), timeout=300)
            return resp.status_code
        except requests.Timeout as e:
            logger.error('Got timeout while trying to post results of predict job:', e)
