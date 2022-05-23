import unittest
import datetime
import json

from app.providers.jobcontainer import JobcontainerProvider
from app.db_models.jobcontainer import db_JobContainer
from app import db

from ..testdata import TestData

class JobcontainerProviderTest(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_mapper(self):
        JP = JobcontainerProvider()
        jobcontainer = JP.mapper(TestData.db_jobcontainer)

        #test values
        self.assertEqual(jobcontainer.callbackUrl, TestData.db_jobcontainer.callbackUrl)
        #Todo: test timestamp

        #test mljob
        mljob = jobcontainer.mljob

        self.assertEqual(mljob.status, TestData.db_mljob.status)
        self.assertEqual(mljob.type, TestData.db_mljob.type)

    def test_post_jobcontainer(self):
        JP = JobcontainerProvider()
        JP.post(TestData.jobcontainer)
        db_jobcontainer = db_JobContainer.query.get(1)
        
        # test values
        self.assertEqual(db_jobcontainer.callbackUrl,
                    TestData.jobcontainer['callbackUrl'])
        #assertEqual(db_Jobcontainer.timestamp, data.jobcontainer['timestamp'])
        #Todo: implement timestamp test

        # test wether mljob was posted
        self.assertIsNotNone(db_jobcontainer.job)

    def test_get_jobcontainer(self):
        JP = JobcontainerProvider()
        db_jobcontainer = db_JobContainer(callbackUrl="www.test.te",
                                       timestamp=datetime.datetime.utcnow())
        db.session.add(db_jobcontainer)

        jobcontainer = json.loads(JP.get(1))

        self.assertEqual(db_jobcontainer.callbackUrl, jobcontainer['callbackUrl'])
        self.assertEqual(str(db_jobcontainer.timestamp), jobcontainer['timestamp'])
