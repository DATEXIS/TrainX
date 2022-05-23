import unittest
import json

from app.providers.session import SessionProvider
from app.db_models.session import db_Session
from app import db

from ..testdata import TestData

class SessionProviderTest(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_mapper(self):
        SP = SessionProvider()
        session = SP.mapper(TestData.db_session)

        #test values
        self.assertEqual(session.title, TestData.db_session.title)
        self.assertEqual(session.description, TestData.db_session.description)

        #test jobcontainer(s)
        jobcontainer = session.jobs[0]
        self.assertEqual(jobcontainer.callbackUrl, TestData.db_jobcontainer.callbackUrl)

        #test sample(s)
        sample = session.samples[0]
        self.assertEqual(TestData.db_sample.begin, sample.begin)
        self.assertEqual(TestData.db_sample.language, sample.language)
        self.assertEqual(TestData.db_sample.length, sample.length)
        self.assertEqual(TestData.db_sample.text, sample.text)
        self.assertEqual(TestData.db_sample.title, sample.title)
        self.assertEqual(TestData.db_sample.type, sample.type)

    def test_post_session(self):
        SP = SessionProvider()
        SP.post(TestData.session)
        db_session = db_Session.query.get(1)

        # test values
        self.assertEqual(db_session.title, TestData.session['title'])
        self.assertEqual(db_session.description, TestData.session['description'])

        # check jobs
        lenj1 = len(db_session.jobs)
        lenj2 = len(TestData.session['jobs'])
        self.assertEqual(lenj1, lenj2)

        # check samples
        lens1 = len(db_session.samples)
        lens2 = len(TestData.session['samples'])
        self.assertEqual(lens1, lens2)

    def test_get_session(self):
        SP = SessionProvider()
        db_session = db_Session(title="Test Session",
                                description="this is a test session")
        db.session.add(db_session)
        db.session.commit()

        session = json.loads(SP.get(1))

        self.assertEqual(db_session.title, session['title'])
        self.assertEqual(db_session.description, session['description'])
