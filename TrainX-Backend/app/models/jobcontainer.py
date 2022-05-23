import copy
import json
from datetime import datetime

import texoopy
from app.models.mljob import MLJob


class JobContainer(texoopy.Span):

    def __init__(self, **kwargs):
        # don't know how to do typehints with custom class correctly
        self.uid: int = kwargs.get('uid', None)
        self.mljob = kwargs.get('mljob', None)
        self.callbackUrl = kwargs.get('callbackUrl')
        self.timestamp = kwargs.get('timestamp', datetime.utcnow())
        self.session_id = kwargs.get('session_id', None)

    def to_texoo_dict(self) -> dict:
        content = copy.deepcopy(self.__dict__)
        timestamp = str(content.pop('timestamp'))
        content['class'] = 'JobContainer'
        content['timestamp'] = timestamp
        return content

    def to_json(self):
        content = self.to_texoo_dict()
        return json.dumps(content, default=lambda o: o.to_texoo_dict())

    @classmethod
    def from_json(cls, json_data: dict):
        json_data = copy.deepcopy(json_data)
        if json_data['class'] != 'JobContainer':
            raise NotAValidJobcontainerException('Supplied json_data is not valid')

        mljob_json = json_data.pop('mljob')
        mljob = MLJob.from_json(mljob_json)
        jobcontainer = cls(**json_data)
        jobcontainer.mljob = mljob
        return jobcontainer
