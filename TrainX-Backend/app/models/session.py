import copy
import json

from app.models.jobcontainer import JobContainer


#from app.models.sample import Sample


class Session(object):

    def __init__(self, **kwargs):
        self.session_id: int = kwargs.get('session_id', None)
        self.title: str = kwargs.get('title')
        self.description: str = kwargs.get('description')
        self.jobs: str = kwargs.get('jobs', None)

    def to_texoo_dict(self) -> dict:
        content = copy.deepcopy(self.__dict__)
        # content.pop('uid')
        content['class'] = 'Session'
        return content

    def to_json(self):
        content = self.to_texoo_dict()
        return json.dumps(content, default=lambda o: o.to_texoo_dict())

    @classmethod
    def from_json(cls, json_data):
        json_data = copy.deepcopy(json_data)
        if json_data['class'] != 'Session':
            raise NotAValidSessionexception('Supplied json_data is not valid')

        jobs_json = json_data.pop('jobs')
        jobs = []

        for job_json in jobs_json:
            jobs.append(JobContainer.from_json(job_json))

        session = cls(**json_data)
        session.jobs = jobs

        return session
