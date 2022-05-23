import json
import os
from datetime import datetime

from app import db
from app.db_models.dataset import db_Dataset
from app.db_models.jobcontainer import db_JobContainer
from app.db_models.mljob import db_MLJob
from app.db_models.model import db_Model
from app.providers.dataset import DatasetProvider
from app.providers.jobcontainer import JobcontainerProvider
from app.routes.backend_ml.commit_job import commit_job

from . import frontend


@frontend.route('/session/<session_id>/startJob', methods=['POST'])
def start_job(session_id):
    """Sends a jobcontainer to the ml component.
       This jobcontainer contains the last used dataset
       The contained mljob is of tye TRAIN"""

    # get last used dataset( the last dataset that was uploaded for now)
    DP = DatasetProvider()
    db_dataset = db_Dataset.query.order_by(db_Dataset.uid.desc()).first()
    dataset = DP.mapper(db_dataset)

    # create mljob( first a db_mljob is created so it can be assigned an id
    # model is the last used model (may use timestamp instead of uid)
    db_model = db.session.query(db_Model).\
                join(db_MLJob).\
                join(db_JobContainer).\
                filter(db_JobContainer.session_id == session_id).\
                filter(db_JobContainer.uid == db_MLJob.container_id).\
                filter(db_MLJob.uid == db_Model.job_id).\
                order_by(db_Model.uid.desc()).first()

    db_mljob = db_MLJob(status="CREATED",
                  type="TRAIN",
                  dataset=db_dataset,
                  model=db_model)
    db.session.add(db_mljob)

    # create JobContainer
    callbackUrl = os.environ['BACKEND_URL'] + "/trainerv2/getJob"
    db_jobcontainer = db_JobContainer(callbackUrl=callbackUrl,
                                    session_id=session_id,
                                    timestamp=datetime.utcnow(),
                                    job=db_mljob)
    db.session.add(db_jobcontainer)
    db.session.commit()

    JP = JobcontainerProvider()

    exit_code = commit_job(json.loads(JP.get(db_jobcontainer.uid)))
    return {"status": exit_code}
