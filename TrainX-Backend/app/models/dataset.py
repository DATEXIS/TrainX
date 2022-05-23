import copy

import texoopy
from app.models.document import Document


class Dataset(texoopy.Dataset):
    def to_texoo_dict(self) -> dict:
        content = copy.deepcopy(self.__dict__)
        return content

    def __init__(self, **kwargs):
        self.uid: int = kwargs.get('uid')
        self.name: str = kwargs.get('name')
        self.language: str = kwargs.get('language')
        self.documents: list = kwargs.get('documents', [])

    @classmethod
    def from_json(cls, json_data: dict):
        json_data = copy.deepcopy(json_data)
        docs = json_data.pop('documents', [])
        dataset = cls(**json_data)
        for doc_json_data in docs:
            dataset.documents.append(Document.from_json(doc_json_data))
        return dataset
