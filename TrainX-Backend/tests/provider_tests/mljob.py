import unittest
import json

from app.providers.mljob import MljobProvider
from app.providers.jobcontainer import db_JobContainer
from app.db_models.mljob import db_MLJob
from app import db

from ..testdata import TestData

class MljobProviderTest(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_mapper(self):
        MP = MljobProvider()
        mljob = MP.mapper(TestData.db_mljob)

        #test values
        self.assertEqual(mljob.status, TestData.db_mljob.status)
        self.assertEqual(mljob.type, TestData.db_mljob.type)

        #test dataset
        dataset = mljob.dataset

        self.assertEqual(dataset.name, TestData.db_dataset.name)
        self.assertEqual(dataset.language, TestData.db_dataset.language)

        #test model
        model = mljob.model

        self.assertEqual(model.binary, TestData.db_model.binary)
        self.assertEqual(model.type, TestData.db_model.type)

    def test_post_mljob(self):
        MP = MljobProvider()
        MP.post(TestData.mljob)
        db_mljob = db_MLJob.query.get(1)

        # test values
        self.assertEqual(db_mljob.status, TestData.mljob['status'])
        self.assertEqual(db_mljob.type, TestData.mljob['type'])

        # test wether dataset and model exist
        self.assertIsNotNone(db_mljob.dataset)
        self.assertIsNotNone(db_mljob.model)

    def test_get_mljob(self):
        MP = MljobProvider()
        db_mljob = db_MLJob(status="being tested",
                            type="test type")
        db.session.add(db_mljob)
        db.session.commit()

        mljob = json.loads(MP.get(1))

        self.assertEqual(db_mljob.status, mljob['status'])
        self.assertEqual(db_mljob.type, mljob['type'])
