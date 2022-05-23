import json

from app import db
from app.db_models.dataset import db_Dataset
from app.models.dataset import Dataset
from app.providers.document import DocumentProvider
from app.routes.responses import Standard404ErrorResponse


class DatasetProvider(object):
    # maps a db_Dataset obj to a Datset obj
    def mapper(self, db_dataset):
        if not db_Dataset:
            return None
        documents = self.getDocuments(db_dataset)
        return Dataset( uid=db_dataset.uid,
                        name=db_dataset.name,
                        language=db_dataset.language,
                        documents=documents)

    # returns the Documents assoziated with the Dataset as a list
    def getDocuments(self, db_dataset):
        documents = []
        DP = DocumentProvider()
        for db_document in db_dataset.documents:
            document = DP.mapper(db_document)
            documents.append(document)

        return documents

    # querys and returns a Dataset obj by its id
    def get(self, uid):
        db_dataset = db_Dataset.query.get(uid)
        if not db_dataset:
            Standard404ErrorResponse()
        dataset = self.mapper(db_dataset)
        return dataset.to_json()

    # writes a Dataset obj to the db and appends it to the provided session
    def post_to_session(self, json_dataset, db_session):
        db_dataset = db_Dataset(name=json_dataset['name'],
                                language=json_dataset['language'])

        db_dataset.session = db_session

        db.session.add(db_dataset)
        db.session.commit()

        if json_dataset['documents']:
            db_dataset = db_Dataset.query.order_by(db_Dataset.uid.desc()).first()
            DP = DocumentProvider()
            for document in json_dataset['documents']:
                DP.post(document, db_dataset)

    # writes a Dataset obj to the db and appends it to the provided mljob
    def post_to_mljob(self, json_dataset, db_mljob):
        db_dataset = db_Dataset(name=json_dataset.get('name'),
                                language=json_dataset.get('language'))

        db_dataset.mljob = db_mljob
        db.session.add(db_dataset)
        db.session.commit()

        if json_dataset.get('documents'):
            db_dataset = db_Dataset.query.order_by(db_Dataset.uid.desc()).first()
            DP = DocumentProvider()
            for document in json_dataset.get('documents', []):
                DP.post(document, db_dataset)

    # yanks a dataset from a session and adds it to a MLJob
    def to_mljob(self, db_session, db_mljob):
        db_dataset = db_session.dataset

        db_dataset.session_id = None
        db_dataset.mljob = db_mljob

        db.session.add(db_dataset)
        db.session.commit()

    def update(self, dataset_json):
        dataset_json = json.loads(dataset_json)
        uid = dataset_json['uid']
        db_dataset = db_Dataset.query.get(uid)

        db_dataset.name = dataset_json['name']
        db_dataset.language = dataset_json['language']

        db.session.commit()

        for document_json in dataset_json['documents']:
            DP = DocumentProvider()
            document_json = json.dumps(document_json)
            DP.update(document_json)
