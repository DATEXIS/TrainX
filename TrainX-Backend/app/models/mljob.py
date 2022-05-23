import copy
import json

import texoopy
from app.models.dataset import Dataset


class MLJob(texoopy.Span):

    def __init__(self, **kwargs):
        self.uid: int = kwargs.get('uid', None)
        self.dataset = kwargs.get('dataset', None)
        self.model = kwargs.get('model', None)
        self.status: str = kwargs.get('status')
        self.type: str = kwargs.get('type')

    def to_texoo_dict(self) -> dict:
        content = copy.deepcopy(self.__dict__)
        #content.pop('model')
        content['class'] = 'MLJob'
        return content

    def to_json(self):
        content = self.to_texoo_dict()
        return json.dumps(content, default=lambda o: o.to_texoo_dict())

    @classmethod
    def from_json(cls, json_data: dict):
        json_data = copy.deepcopy(json_data)
        if json_data.get('class') != 'MLJob':
            raise NotAValidMljobException('Supplied JSON is not valid')

        dataset = Dataset.from_json(json_data.pop('dataset'))
        mljob = cls(**json_data)
        mljob.dataset = dataset
        return mljob
