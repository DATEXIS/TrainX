import base64
import copy
import json
import os
import tarfile
import tempfile
from datetime import datetime
from enum import Enum
from typing import List, Union

from texoopy import Dataset


class B64TarWrapper:

    def __init__(self, identifier: str, tar_base64: str):
        self.identifier: str = identifier
        self.tar_base64: str = tar_base64

    @classmethod
    def from_files(cls, paths: List[str], identifier: Union[str, None] = None):
        tar_file = tempfile.mktemp()
        with tarfile.open(tar_file, 'x') as tar:
            for path in paths:
                tar.add(path, arcname=os.path.basename(path))
        with open(tar_file, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        return cls(identifier=identifier, tar_base64=encoded)

    def get_extract(self, directory: Union[str, None] = None) -> str:
        """
        Extracts the content into a temporary directory and returns the path as string
        :param directory: If given, extraction will take place in this directory
        :return: Path as string
        """
        temp_tar_file = tempfile.NamedTemporaryFile()
        with open(temp_tar_file.name, 'wb') as f:
            f.write(base64.b64decode(self.tar_base64))

        if directory is None:
            directory = tempfile.mkdtemp()

        with tarfile.open(temp_tar_file.name, 'r') as tar:
            for member in tar.getmembers():
                tar.extract(member, directory)

        return directory

    def get_base64_str(self) -> str:
        return self.tar_base64


class JobType(Enum):
    TRAIN = 1
    PREDICT = 2

    def to_texoo_dict(self):
        return self.name


class JobStatus(Enum):
    RUNNING = 1
    FINISHED = 2
    NEW = 3
    QUEUED = 4
    CREATED = 5

    def to_texoo_dict(self):
        return self.name


class MLModel:
    def __init__(self, binary: str, type: str = '', edited: str = str(datetime.utcnow()), **kwargs):
        self.binary = binary
        self.type = type
        self.edited = edited

    @classmethod
    def from_json(cls, json_data: dict):
        json_data = copy.deepcopy(json_data)
        return cls(**json_data)

    def to_json(self):
        return json.dumps(self.to_texoo_dict(), default=lambda o: o.to_texoo_dict())

    def to_texoo_dict(self) -> dict:
        return self.__dict__


class Job:
    def __init__(self, uid: int, type: JobType, status: JobStatus, dataset: Dataset, model: MLModel = None, **kwargs):
        self.uid = uid
        self.type = type
        self.status = status
        self.dataset = dataset
        self.model = model

    @classmethod
    def from_json(cls, json_data: dict):
        json_data = copy.deepcopy(json_data)
        json_data['type'] = JobType[json_data['type']]
        json_data['status'] = JobStatus[json_data['status']]
        json_data['dataset'] = Dataset.from_json(json_data['dataset']) if json_data['dataset'] is not None else None
        json_data['model'] = MLModel.from_json(json_data['model']) if json_data['model'] is not None else None
        return cls(**json_data)

    def to_json(self):
        return json.dumps(self.to_texoo_dict(), default=lambda o: o.to_texoo_dict())

    def to_texoo_dict(self) -> dict:
        return self.__dict__


class JobContainer:

    def __init__(self, mljob: Job, callbackUrl: str, **kwargs):
        self.mljob = mljob
        self.callbackUrl = callbackUrl

    @classmethod
    def from_json(cls, json_data: dict):
        json_data = copy.deepcopy(json_data)
        json_data['mljob'] = Job.from_json(json_data['mljob'])
        return cls(**json_data)

    def to_json(self):
        return json.dumps(self.to_texoo_dict(), default=lambda o: o.to_texoo_dict())

    def to_texoo_dict(self) -> dict:
        return self.__dict__
