import json
import os
from datetime import datetime

from app import app
from app import db
from app.db_models.dataset import db_Dataset
from app.db_models.jobcontainer import db_JobContainer
from app.db_models.mljob import db_MLJob
from app.db_models.model import db_Model
from app.providers.dataset import DatasetProvider
from app.providers.jobcontainer import JobcontainerProvider
from app.routes.backend_ml.commit_job import commit_job
from flask import request

from . import ml_component


@ml_component.route('/getJob', methods=['POST'])
def get_job():
    """receives a job from the ml_component"""
    job_container = json.loads(request.json)
    JP = JobcontainerProvider()

    # if job.tye ins TRAIN save the container and send a predict job containing the
    # model and the latest dataset
    if job_container['mljob']['type'] == 'TRAIN':
        app.logger.warning("received finished TRAIN job")

        # get the session the jobcontainer should be saved to
        uid = job_container['mljob']['uid']
        db_session = db_MLJob.query.get(uid).jobcontainer.session

        # save the jobcontainer
        JP.post(job_container, db_session)

        # create predict job
        callbackUrl = os.environ['BACKEND_URL']+"/trainerv2/getJob"

        db_model = db.session.query(db_Model).\
            join(db_MLJob).\
            join(db_JobContainer).\
            filter(db_JobContainer.session_id == db_session.uid).\
            filter(db_JobContainer.uid == db_MLJob.container_id).\
            filter(db_MLJob.uid == db_Model.job_id).\
            order_by(db_Model.uid.desc()).first()
        db_dataset = db.session.query(db_Dataset).\
            filter(db_Dataset.session_id == db_session.uid).first()
        db_mljob = db_MLJob(
            status="CREATED",
            type="PREDICT",
            dataset=db_dataset,
            model=db_model)
        db_jobcontainer = db_JobContainer(
            callbackUrl=callbackUrl,
            session_id=db_session.uid,
            timestamp=datetime.utcnow(),
            job=db_mljob)
        db.session.add_all([db_mljob, db_jobcontainer])
        db.session.commit()

        JP = JobcontainerProvider()
        jobcontainer = JP.mapper(db_jobcontainer)
        payload = json.loads(jobcontainer.to_json())

        # start predict job
        commit_job(payload)
        return {'status':200}

    # if the job.type is PREDICT save the Dataset
    elif job_container['mljob']['type'] == 'PREDICT':
        app.logger.warning("received finished PREDICT job")
        # the dataset with predictions
        dataset_json = job_container['mljob']['dataset']

        # post the dataset to the appropiate session
        uid = job_container['mljob']['uid']
        db_session = db_MLJob.query.get(uid).jobcontainer.session
        DP = DatasetProvider()
        DP.post_to_session(dataset_json, db_session)
        return {'status':200}

    else:
        return {'status':500}
