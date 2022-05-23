import unittest
import json
from datetime import datetime

from app.db_models.session import db_Session
from app.db_models.jobcontainer import db_JobContainer
from app.db_models.mljob import db_MLJob
from app.db_models.model import db_Model
from app.db_models.sample import db_Sample
from app.db_models.mention_annotation import db_MentionAnnotation
from app.db_models.named_entity_annotation import db_NamedEntityAnnotation

from app.routes.frontend_backend.get_model import get_model
from app.routes.frontend_backend.get_models import get_models
from app.routes.frontend_backend.get_samples import get_samples
from app.routes.frontend_backend.get_session import get_session
from app.routes.frontend_backend.get_sessions import get_sessions
from app import db

class Test_get_endpoints(unittest.TestCase):
    def setUp(self):
        db.create_all()

        annotation1 = db_MentionAnnotation(confidence=1)
        annotation2 = db_NamedEntityAnnotation(confidence=2)
        annotation3 = db_MentionAnnotation(confidence=3)
        annotation4 = db_NamedEntityAnnotation(confidence=4)

        sample1 = db_Sample(text="sample1",
                            items=[annotation1, annotation3])
        sample2 = db_Sample(text="sample2",
                            items=[annotation2, annotation4])
        model1 = db_Model(binary="asdf",
                          type="wrong model",
                          edited=datetime.utcnow())
        model2 = db_Model(type="correct model",
                          binary="ghjk",
                          edited=datetime.utcnow())
        mljob1 = db_MLJob(status="first mljob",
                          type="testMljob1",
                          model=model1)
        mljob2 = db_MLJob(status="second mljob",
                          type="testMljob2",
                          model=model2)
        jobcontainer1 = db_JobContainer(timestamp=datetime.utcnow(),
                                       job=mljob1,
                                       callbackUrl="1.container.de")
        jobcontainer2 = db_JobContainer(timestamp=datetime.utcnow(),
                                       job=mljob2,
                                       callbackUrl="2.container.de")
        session1 = db_Session(title="FirstSession")
        session2 = db_Session(title="SecondSession",
                             jobs=[jobcontainer1, jobcontainer2],
                             samples=[sample1, sample2])

        db.session.add(session1)
        db.session.add(session2)
        db.session.add_all([model1,model2,mljob1,mljob2,jobcontainer1,
                            jobcontainer2,annotation1,
                            annotation2, annotation3, annotation4,
                            sample1, sample2])
        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_get_model(self):
        # get_model should return model2 since it's in mljob2 which is in
        # jobcontainer2 which is the last created jobcontainer in session2

        session_id = 2
        model = get_model(session_id)
        model_json = json.loads(model)
        self.assertEqual(model_json['type'], "correct model")

    def test_get_models(self):
        session_id = 2
        models_json = json.loads(get_models(session_id))

        model1 = models_json[0]
        model2 = models_json[1]

        self.assertEqual(model1['binary'], "asdf")
        self.assertEqual(model2['binary'], "ghjk")

    def test_get_samples(self):
        session_id = 2
        samples = json.loads(get_samples(session_id))

        self.assertEqual(samples[0]['text'], "sample1")
        self.assertEqual(samples[1]['text'], "sample2")

    def test_get_session(self):
        """ Test wether """
        session_id = 2
        session = json.loads(get_session(session_id))

        self.assertEqual(session['title'], "SecondSession")

    def test_get_sessions_not_empty(self):
        """ Test wether get_sesisons loads all 2 sessions"""
        sessions = json.loads(get_sessions())

        self.assertEqual(len(sessions), 2)

    def test_get_sessions_empty(self):
        """ Test wether get_sessions returns None if there are 0 sessions"""
        db_Session.query.delete()
        self.assertIsNone(get_sessions())
