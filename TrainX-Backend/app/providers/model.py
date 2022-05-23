import json
import os
import uuid
from datetime import datetime

from app import db
from app.db_models.mljob import db_MLJob
from app.db_models.model import db_Model


class ModelProvider(object):

    def get(self, id):
        """Returns the model associated with the id"""
        path = db_Model.query.get(id).path
        with open(path) as f:
            return json.load(f)

    def post(self, model_json, db_mljob):
        """Writes the model to a file and saves it's path to db"""

        if not os.path.exists("/var/lib/TraiNER/models"):
            os.makedirs("/var/lib/TraiNER/models")

        filename = "/var/lib/TraiNER/models/" + str(uuid.uuid4())
        with open(filename, "w") as f:
            json.dump(model_json, f)

        db_model = db_Model(path=filename,
                            edited=datetime.utcnow())

        db_mljob = db_MLJob.query.get(db_mljob.uid)
        db_model.mljob = db_mljob

        db.session.add(db_model)
        db.session.commit()
