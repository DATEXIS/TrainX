import copy

import texoopy


class Model(texoopy.Span):
    def __init__(self, **kwargs):
        self.uid: int = kwargs.get('uid', None)
        self.binary = kwargs.get('binary')
        self.type: str = kwargs.get('type')
        self.edited = kwargs.get('edited', None)

    def to_texoo_dict(self) -> dict:
        content = copy.deepcopy(self.__dict__)
        edited = content.pop('edited')
        content['edited'] = str(edited)
        return content
