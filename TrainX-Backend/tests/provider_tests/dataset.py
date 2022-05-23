import unittest
import json

from app.providers.dataset import DatasetProvider
from app.db_models.dataset import db_Dataset
from app.db_models.mljob import db_MLJob
from app.db_models.session import db_Session
from app import db

from ..testdata import TestData


class DatasetProviderTest(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_mapper(self):
        DP = DatasetProvider()
        dataset = DP.mapper(TestData.db_dataset)

        #test values
        self.assertEqual(dataset.name, TestData.db_dataset.name)
        self.assertEqual(dataset.language, TestData.db_dataset.language)

        #test documents
        document = dataset.documents[0]

        self.assertEqual(document.begin, TestData.db_document.begin)
        self.assertEqual(document.length, TestData.db_document.length)
        self.assertEqual(document.text, TestData.db_document.text)
        self.assertEqual(document.id, TestData.db_document.id)
        self.assertEqual(document.title, TestData.db_document.title)
        self.assertEqual(document.type, TestData.db_document.type)

    def test_post_to_session(self):
        DP = DatasetProvider()
        session = db_Session()
        DP.post_to_session(TestData.dataset, session)

        db_dataset = db_Dataset.query.get(1)

        # test values
        self.assertEqual(db_dataset.name, TestData.dataset['name'])
        self.assertEqual(db_dataset.language, TestData.dataset['language'])

        #test wether number of documents is the same
        len1 = len(db_dataset.documents.all())
        len2 = len(TestData.dataset['documents'])
        self.assertEqual(len1, len2)

    def test_post_to_mljob(self):
        DP = DatasetProvider()
        mljob = db_MLJob()
        DP.post_to_mljob(TestData.dataset, mljob)

        db_dataset = db_Dataset.query.get(1)

        self.assertEqual(db_dataset.name, TestData.dataset['name'])
        self.assertEqual(db_dataset.language, TestData.dataset['language'])

    def test_get_dataset(self):
        DP = DatasetProvider()
        db_dataset = db_Dataset(name="Test Dataset",
                             language="eng")
        db.session.add(db_dataset)
        db.session.commit()

        dataset = json.loads(DP.get(1))

        self.assertEqual(db_dataset.name, dataset['name'])
        self.assertEqual(db_dataset.language, dataset['language'])
