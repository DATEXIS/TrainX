import unittest
import json

from app.providers.annotation import AnnotationProvider
from app.db_models.annotation import db_Annotation
from app.db_models.mention_annotation import db_MentionAnnotation
from app.db_models.named_entity_annotation import db_NamedEntityAnnotation
from app import db

from ..testdata import TestData

class AnnotationProviderTest(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_mapper_mention(self):
        AP = AnnotationProvider()
        mention = AP.mapper(TestData.db_mention)

        self.assertEqual(TestData.db_mention.begin, mention.begin)
        self.assertEqual(TestData.db_mention.length, mention.length)
        self.assertEqual(TestData.db_mention.text, mention.text)
        self.assertEqual(TestData.db_mention.source, mention.source)
        self.assertEqual(TestData.db_mention.confidence, mention.confidence)
        self.assertEqual(TestData.db_mention.type, mention.type)
        self.assertEqual(TestData.db_mention.refId, mention.refId)

    def test_mapper_namedEntity(self):
        AP = AnnotationProvider()

        namedEntity = AP.mapper(TestData.db_namedEntity)

        self.assertEqual(TestData.db_namedEntity.begin, namedEntity.begin)
        self.assertEqual(TestData.db_namedEntity.length, namedEntity.length)
        self.assertEqual(TestData.db_namedEntity.text, namedEntity.text)
        self.assertEqual(TestData.db_namedEntity.source, namedEntity.source)
        self.assertEqual(TestData.db_namedEntity.confidence, namedEntity.confidence)
        self.assertEqual(TestData.db_namedEntity.refId, namedEntity.refId)

    def test_post_mention(self):
        """First post a mention_json to the db, then compare wether it's
        attributes match the mention in the db"""
        AP = AnnotationProvider()
        AP.post(TestData.mentionAnnotation)
        db_mention = db_Annotation.query.get(1)

        self.assertEqual(db_mention.begin, TestData.mentionAnnotation['begin'])
        self.assertEqual(db_mention.length, TestData.mentionAnnotation['length'])
        self.assertEqual(db_mention.text, TestData.mentionAnnotation['text'])
        self.assertEqual(db_mention.source, TestData.mentionAnnotation['source'])
        self.assertEqual(db_mention.confidence, TestData.mentionAnnotation['confidence'])
        self.assertEqual(db_mention.type, TestData.mentionAnnotation['type'])
        self.assertEqual(db_mention.refId, TestData.mentionAnnotation['refId'])

    def test_post_namedEntity(self):
        """First post a mention_json to the db, then compare wether it's
        attributes match the mention in the db"""
        AP = AnnotationProvider()
        AP.post(TestData.namedEntityAnnotation)
        db_namedEntity = db_Annotation.query.get(1)

        self.assertEqual(db_namedEntity.begin, TestData.namedEntityAnnotation['begin'])
        self.assertEqual(db_namedEntity.length, TestData.namedEntityAnnotation['length'])
        self.assertEqual(db_namedEntity.text, TestData.namedEntityAnnotation['text'])
        self.assertEqual(db_namedEntity.source, TestData.namedEntityAnnotation['source'])
        self.assertEqual(db_namedEntity.confidence, TestData.namedEntityAnnotation['confidence'])
        self.assertEqual(db_namedEntity.refId, TestData.namedEntityAnnotation['refId'])

    def test_get_mention(self):
        AP = AnnotationProvider()
        db_mention = db_MentionAnnotation(begin=0, length=100, text="This is a mention",
                                       source="test source",
                                       confidence=5, type="mention",
                                       refId="refId")
        db.session.add(db_mention)
        db.session.commit()
        
        mention = json.loads(AP.get(1))
        self.assertEqual(mention['begin'], db_mention.begin)
        self.assertEqual(mention['length'], db_mention.length)
        self.assertEqual(mention['text'], db_mention.text)
        self.assertEqual(mention['source'], db_mention.source)
        self.assertEqual(mention['confidence'], db_mention.confidence)
        self.assertEqual(mention['type'], db_mention.type)
        self.assertEqual(mention['refId'], db_mention.refId)

    def test_get_namedEntity(self):
        AP = AnnotationProvider()
        db_namedEntity = db_NamedEntityAnnotation(begin=0,
                                       length=100, text="This is a mention",
                                       source="test source",
                                       confidence=5,
                                       refId="refId")
        db.session.add(db_namedEntity)
        db.session.commit()

        namedEntity = json.loads(AP.get(1))
        self.assertEqual(db_namedEntity.begin, namedEntity['begin'])
        self.assertEqual(db_namedEntity.length, namedEntity['length'])
        self.assertEqual(db_namedEntity.text, namedEntity['text'])
        self.assertEqual(db_namedEntity.source, namedEntity['source'])
        self.assertEqual(db_namedEntity.confidence, namedEntity['confidence'])
        self.assertEqual(db_namedEntity.refId, namedEntity['refId'])


