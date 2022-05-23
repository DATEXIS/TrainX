import copy

import texoopy
from app.models.annotation import Annotation


class Document(texoopy.Document):
    def to_texoo_dict(self) -> dict:
        content = copy.deepcopy(self.__dict__)
        content['class'] = 'Document'
        return content

    def __init__(self, **kwargs):
        # we don't have a class for sentences yet
        super().__init__(**kwargs)

    @classmethod
    def from_json(cls, json_data: dict, do_sentence_splitting=False):
        json_data = copy.deepcopy(json_data)
        if json_data.get('class') != 'Document':
            raise NotATeXooDocumentException('Supplied JSON is not a valid TeXoo document.')

        annotations = []
        for json_data_annotation in json_data.get('annotations', []):
            annotations.append(Annotation.from_json(json_data_annotation))
        json_data['annotations'] = annotations

        if do_sentence_splitting:
            raise NotImplementedError("Sentence splitting is not implemented yet.")  # TODO add sentence splitting

        return cls(**json_data)
