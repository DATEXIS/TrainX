import json

from app.db_models.session import db_Session
from app.providers.dataset import DatasetProvider
from app.routes.responses import Standard200Response
from flask import request

from . import frontend


@frontend.route('/session/<session_id>/uploadDataset',
                methods=['POST'])
def upload_dataset(session_id):
    """add a dataset to the provided Session"""

    req_data = request.files['dataset'].read()
    as_json = json.loads(req_data)

    db_session = db_Session.query.get(session_id)

    DP = DatasetProvider()
    DP.post_to_session(as_json, db_session)

    return Standard200Response("Dataset uploaded\n")
