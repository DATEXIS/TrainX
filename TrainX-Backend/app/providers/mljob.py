import json

from app import db
from app.db_models.mljob import db_MLJob
from app.models.mljob import MLJob
from app.providers.dataset import DatasetProvider
from app.providers.model import ModelProvider
from app.routes.responses import Standard404ErrorResponse


class MljobProvider(object):
    # maps a db_MLJob to a MLJob obj
    def mapper(self, db_MLJob):
        if not db_MLJob:
            return None

        DP = DatasetProvider()
        MP = ModelProvider()
        if db_MLJob.model:
            model = MP.get(db_MLJob.model.uid)
        else:
            model = None

        if db_MLJob.dataset:
            dataset = DP.mapper(db_MLJob.dataset)
        else:
            dataset = None

        return MLJob(status=db_MLJob.status,
                     type=db_MLJob.type,
                     uid=db_MLJob.uid,
                     dataset=dataset,
                     model=model)

    # querys and returns an MLJob by id
    def get(self, id):
        db_mljob = db_MLJob.query.get(id)
        if not db_mljob:
            Standard404ErrorResponse()
        job = self.mapper(db_mljob)
        return job.to_json()

    # writes a MLJob obj to the db and links it to a JobContainer
    def post(self, mljob_json, db_jobcontainer=None):

        db_mljob = db_MLJob(status=mljob_json['status'],
                            type=mljob_json['type'],
                            jobcontainer=db_jobcontainer)

        db.session.add(db_mljob)
        db.session.commit()
        db_mljob = db_MLJob.query.order_by(db_MLJob.uid.desc()).first()

        if mljob_json['dataset']:
            DP = DatasetProvider()
            DP.post_to_mljob(mljob_json['dataset'], db_mljob)
        if mljob_json['model']:
            MP = ModelProvider()
            MP.post(mljob_json['model'], db_mljob)

    def update(self, mljob_json):
        #mljob_json = json.loads(mljob_json)
        uid = mljob_json['uid']

        db_mljob = db_MLJob.query.get(uid)

        db_mljob.status = mljob_json['status']
        db_mljob.type = mljob_json['type']
        db.session.commit()


        if mljob_json['dataset']:
            dataset_json = mljob_json['dataset']
            DP = DatasetProvider()
            if db_mljob.dataset:
                DP.update(json.dumps(mljob_json['dataset']))
            else:
                DP.post_to_mljob(dataset_json, db_mljob)

        if mljob_json['model']:
            model_json = mljob_json['model']
            MP = ModelProvider()
            if db_mljob.model:
                MP.update(model_json)
            else:
                model_json = {'binary': model_json, 'type':'model'}
                MP.post(model_json, db_mljob)

