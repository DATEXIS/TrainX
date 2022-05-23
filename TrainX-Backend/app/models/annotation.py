import copy

import texoopy


class Annotation(texoopy.Annotation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_texoo_dict(self) -> dict:
        content = copy.deepcopy(self.__dict__)
        content['class'] = "SimpleAnnotation"
        return content
