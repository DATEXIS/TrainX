import unittest
import json

from app.providers.document import DocumentProvider
from app.db_models.document import db_Document
from app.db_models.dataset import db_Dataset
from app import db

from ..testdata import TestData

class DocumentProviderTest(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_mapper(self):
        DP = DocumentProvider()
        document = DP.mapper(TestData.db_document)

        # test values
        self.assertEqual(document.begin, TestData.db_document.begin)
        self.assertEqual(document.length, TestData.db_document.length)
        self.assertEqual(document.text, TestData.db_document.text)
        self.assertEqual(document.id, TestData.db_document.id)
        self.assertEqual(document.title, TestData.db_document.title)
        self.assertEqual(document.type, TestData.db_document.type)

        # test annotations
        namedEntity = document.annotations[0]
        mention = document.annotations[1]

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

    def test_post_document(self):
        DP = DocumentProvider()
        DP.post(TestData.document1)

        db_document = db_Document.query.get(1)

        # test values
        self.assertEqual(db_document.begin, TestData.document1['begin'])
        self.assertEqual(db_document.length, TestData.document1['length'])
        self.assertEqual(db_document.text, TestData.document1['text'])
        self.assertEqual(db_document.id, TestData.document1['id'])
        self.assertEqual(db_document.title, TestData.document1['title'])
        self.assertEqual(db_document.type, TestData.document1['type'])

        # test wether number of annotations is the same
        len1 = len(db_document.annotations.all())
        len2 = len(TestData.document1['annotations'])
        self.assertEqual(len1, len2)

    def test_get_document(self):
        DP = DocumentProvider()
        db_document = db_Document(id="id",
                               language="eng",
                               begin=99,
                               length=100,
                               title="title",
                               type="type",
                               text="texttexttext")
        db.session.add(db_document)
        db.session.commit()

        document = json.loads(DP.get(1))

        self.assertEqual(db_document.id , document['id'])
        self.assertEqual(db_document.language , document['language'])
        self.assertEqual(db_document.begin , document['begin'])
        self.assertEqual(db_document.length , document['length'])
        self.assertEqual(db_document.title , document['title'])
        self.assertEqual(db_document.type , document['type'])
        self.assertEqual(db_document.text , document['text'])
