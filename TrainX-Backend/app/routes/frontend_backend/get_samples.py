from app import db
from app.db_models.dataset import db_Dataset
from app.db_models.document import db_Document
from app.db_models.session import db_Session
from app.providers.document import DocumentProvider
from flask import request

from . import frontend


@frontend.route('/session/<session_id>/samples', methods=['GET'])
# returns a list of samples
def get_samples(session_id):
    """Returns a list of Document-jsons belonging to the latest Dataset in db_Session(session_id)
    ordered ascending by the lowest confidence in the Annotaitons belonging to
    said Samples"""
    offset = int(request.args.get('offset'))

    # get the id of the last dataset in session
    dataset_id = db.session.query(db_Dataset).\
                    join(db_Session).\
                    filter(db_Dataset.session_id == session_id).\
                    order_by(db_Dataset.uid.desc()).first().uid

    # get all the documents in pagination range
    db_sample = db.session.query(db_Document).\
            join(db_Dataset).\
            filter(db_Document.dataset_id == dataset_id).\
            order_by(db_Document.avg_confidence.desc()).\
            all()[offset]

    # return the documents as json
    DP = DocumentProvider()
    sample = DP.mapper(db_sample)
    return sample.to_json()
