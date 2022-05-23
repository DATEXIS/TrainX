import os

import requests
from app.db_models.mljob import db_MLJob
from app.providers.model import ModelProvider

from . import ml_component


@ml_component.route('/commitJob', methods=['POST'])
def commit_job(jobcontainer):
    """Sends a jobcontainer dict to the ml component"""

    if jobcontainer['mljob']['type'] == 'TRAIN':
        pass
    if jobcontainer['mljob']['type'] == 'PREDICT':
        # add the model to the jobcontainer
        MP = ModelProvider()
        db_mljob = db_MLJob.query.get(jobcontainer['mljob']['uid'])
        model = jobcontainer['mljob']['model']
        MP.post(model, db_mljob)
    jobcontainer['callbackUrl'] = os.environ['BACKEND_URL'] + "/trainerv2/getJob"

    # send json to ml_component 
    start_job_url = os.environ['ML_URL'] + "/startjob"
    res = requests.post(start_job_url, json=jobcontainer)

    return res.status_code
