from app import db
from app.db_models.annotation import db_Annotation
from app.db_models.document import db_Document
from app.providers.annotation import AnnotationProvider
from app.routes.responses import Standard200Response
from flask import request

from . import frontend


@frontend.route('/session/<session_id>/uploadSamples',
                methods=['POST'])
def upload_samples(session_id):
    """Adds a sample to the most recent dataset in the session"""
    req_data = request.get_json()
    for document in req_data['documents']:

        # first delete all old anntation for the document
        old_samples = db.session.query(db_Annotation).\
                filter(db_Annotation.document_id == document['uid']).all()
        # delete all entries seperatly as SQLAlchemys bulk delete()
        # does not support cascading relationships
        for sample in old_samples:
            db.session.delete(sample)

        # then add the new annotations to the document
        AP = AnnotationProvider()
        db_document = db_Document.query.get(document['uid'])
        for anntation in document['annotations']:
            AP.post(anntation, db_document)
        db.session.commit()

    return Standard200Response("Samples uploaded")
