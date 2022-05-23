import unittest
import json

from app.providers.sample import SampleProvider
from app.db_models.sample import db_Sample
from app import db

from ..testdata import TestData

class SampleProviderTest(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_mapper(self):
        SP = SampleProvider()
        sample = SP.mapper(TestData.db_sample)
        # test values
        self.assertEqual(TestData.db_sample.begin, sample.begin)
        self.assertEqual(TestData.db_sample.language, sample.language)
        self.assertEqual(TestData.db_sample.length, sample.length)
        self.assertEqual(TestData.db_sample.text, sample.text)
        self.assertEqual(TestData.db_sample.title, sample.title)
        self.assertEqual(TestData.db_sample.type, sample.type)

        # test annotations
        namedEntity = sample.annotations[0]
        mention = sample.annotations[1]

        self.assertEqual(TestData.db_mention.begin, mention.begin)
        self.assertEqual(TestData.db_mention.length, mention.length)
        self.assertEqual(TestData.db_mention.text, mention.text)
        self.assertEqual(TestData.db_mention.source, mention.source)
        self.assertEqual(TestData.db_mention.confidence, mention.confidence)
        self.assertEqual(TestData.db_mention.type, mention.type)
        self.assertEqual(TestData.db_mention.refId, mention.refId)

        self.assertEqual(TestData.db_namedEntity.begin, namedEntity.begin)
        self.assertEqual(TestData.db_namedEntity.length, namedEntity.length)
        self.assertEqual(TestData.db_namedEntity.text, namedEntity.text)
        self.assertEqual(TestData.db_namedEntity.source, namedEntity.source)
        self.assertEqual(TestData.db_namedEntity.confidence, namedEntity.confidence)
        self.assertEqual(TestData.db_namedEntity.refId, namedEntity.refId)

    def test_post_sample(self):
        SP = SampleProvider()
        SP.post(TestData.sample)

        db_sample = db_Sample.query.get(1)

        # test values
        self.assertEqual(db_sample.begin, TestData.sample['begin'])
        self.assertEqual(db_sample.language, TestData.sample['language'])
        self.assertEqual(db_sample.length, TestData.sample['length'])
        self.assertEqual(db_sample.text, TestData.sample['text'])
        self.assertEqual(db_sample.type, TestData.sample['class'])

        # test wether the number of annotations is the same
        len1 = len(db_sample.items.all())
        len2 = len(TestData.sample['annotations'])
        self.assertEqual(len1, len2)

    def test_get_sample(self):
        SP = SampleProvider()
        db_sample = db_Sample(begin=987,
                              language="eng",
                              length=145,
                              text="test sample",
                              type="test")
        db.session.add(db_sample)
        db.session.commit()

        sample = json.loads(SP.get(1))

        # test values
        self.assertEqual(db_sample.begin, sample['begin'])
        self.assertEqual(db_sample.language, sample['language'])
        self.assertEqual(db_sample.length, sample['length'])
        self.assertEqual(db_sample.text, sample['text'])
        self.assertEqual(db_sample.type, sample['type'])
