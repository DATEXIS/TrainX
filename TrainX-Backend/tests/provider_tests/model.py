import unittest
import datetime
import json

from app.providers.model import ModelProvider
from app.db_models.model import db_Model
from app.db_models.mljob import db_MLJob
from app import db

from ..testdata import TestData

class ModelProviderTest(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_mapper(self):
        MP = ModelProvider()
        model = MP.mapper(TestData.db_model)

        self.assertEqual(model.binary, TestData.db_model.binary)
        self.assertEqual(model.type, TestData.db_model.type)
        #Todo: test edited

    def test_post_model(self):
        MP = ModelProvider()
        mljob = db_MLJob()
        MP.post(TestData.model, mljob)

        db_model = db_Model.query.get(1)

        self.assertEqual(db_model.binary, TestData.model['binary'])
        self.assertEqual(db_model.type, TestData.model['type'])
        #Todo: implement edited test

    def test_get_model(self):
        MP = ModelProvider()
        db_model = db_Model(binary="asrasheiufghaiuphfgpuha",
                            type="test type",
                            edited=datetime.datetime.utcnow())
        db.session.add(db_model)
        db.session.commit()

        model = json.loads(MP.get(1))

        self.assertEqual(db_model.binary, model['binary'])
        self.assertEqual(db_model.type, model['type'])
        self.assertEqual(str(db_model.edited), model['edited'])
