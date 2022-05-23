import os

import requests
from app import app
from app.db_models.mljob import db_MLJob
from flask import Response

from . import frontend


@frontend.route('/session/<session_id>/status', methods=['GET'])
# returns the status of the train
def get_status(session_id):
    """ Returns the status of the latest MLJob in the session"""

    try:
        job_id = db_MLJob.query.order_by(db_MLJob.uid.desc()).first().uid
    except:
        return Response(status=404)

    url = os.environ['ML_URL'] + "/jobstatus/" + str(job_id)
    app.logger.warning("getting status of job {}".format(job_id))
    res = requests.get(url, timeout=5)

    app.logger.warning(res.status_code)
    if res.status_code != 404:
        app.logger.warning(res.json())
        return Response(
            response = res.json(),
            status = res.status_code,
            headers = dict(res.headers)
            )
    else:
        return Response(
            status = 404
            )
