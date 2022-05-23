from datetime import datetime
import os

os.environ['TESTING'] = 'True'
os.environ['DEBUG'] = 'False'
os.environ['URL_PREFIX'] = '/testing'

from app.db_models.mention_annotation import db_MentionAnnotation
from app.db_models.named_entity_annotation import db_NamedEntityAnnotation
from app.db_models.sample import db_Sample
from app.db_models.document import db_Document
from app.db_models.dataset import db_Dataset
from app.db_models.model import db_Model
from app.db_models.mljob import db_MLJob
from app.db_models.jobcontainer import db_JobContainer
from app.db_models.session import db_Session

class TestData(object):
    mentionAnnotation = {'begin':15, 'length':120,
                        'text':"This is a mention",
                        'source':"This source",
                        'confidence': 5, 'type':"mention",
                        'refId':"Ref", 'class':"MentionAnnotation"}

    namedEntityAnnotation = {'begin':30, 'length':55,
                              'text':"This is a named entity",
                              'source':"This source 2",
                              'confidence': 5, 'refId':"Ref2", 'class':
                              "NamedEntityAnnotation"}

    sample = {'begin':55, 'language':'eng', 'length':200, 
              'text':"This is a sample", 'class':'test sample',
              'class':"test", 'title':"TestSample",
              'annotations': [mentionAnnotation, namedEntityAnnotation]}

    document1 = {'begin':333, 'length':200, 'text':"This is a document 1",
                'id':"Test Id 1", 'title':"Test Document 1", 'type':"TestDoc",
                 'language':"eng", 'class':"document",
                 'annotations':[mentionAnnotation, namedEntityAnnotation]}

    document2 = {'begin':155, 'length':40, 'text':"This is a document 2",
                'id':"Test Id 2", 'title':"Test Document 2", 'type':"TestDoc",
                 'language':"eng", 'class':"dcoument",
                'annotations':[mentionAnnotation, namedEntityAnnotation]}

    dataset = {'name':"Test Dataset", 'language':"eng",
               'documents':[document1, document2]}

    model = {'binary':"ahsudpvgadyga3283yrwefphve9rpgwerg893",
             'type':"test model", 'edited': datetime.utcnow()}

    mljob = {'status': "being tested", 'type':"test type",
             'dataset': dataset, 'model': model}

    # TODO: implement timestamp test
    jobcontainer = {'callbackUrl': "www.test.com",
                    'mljob': mljob}

    session = {'title': "test session", 'description': "this is a test session",
               'jobs':[jobcontainer], 'samples':[sample]}

    db_mention = db_MentionAnnotation(begin=0, 
                                      length=100, 
                                      text="This is a mention",
                                      source="test source",
                                      confidence=3, 
                                      type="mention",
                                      refId="refId")

    db_namedEntity = db_NamedEntityAnnotation(begin=0,
                                   length=100, 
                                   text="This is a mention",
                                   source="test source",
                                   confidence=5,
                                   refId="refId")

    db_sample = db_Sample(begin=99,
                          language="eng",
                          length=100,
                          text="HoHi",
                          title="Test Sample",
                          type="TestType",
                          items=[db_namedEntity, db_mention])

    db_document = db_Document(begin=0,
                              length=90,
                              text="jojojjojo",
                              id="testId",
                              title="TestDocument",
                              language="eng",
                              type="Test type",
                              annotations=[db_namedEntity, db_mention])

    db_dataset = db_Dataset(name="TestDataset",
                            language="eng",
                            documents=[db_document])

    db_model = db_Model(binary="asdvnasuifbnasfbau",
                        type="testType")
                        # also test edited

    db_mljob = db_MLJob(status="testing",
                        type="testType",
                        dataset=db_dataset,
                        model=db_model)

    db_jobcontainer = db_JobContainer(callbackUrl="test.testing.te",
                                      timestamp=datetime.utcnow(),
                                      job=db_mljob)

    db_session = db_Session(title="TestSession",
                            description="this is a test session",
                            jobs=[db_jobcontainer],
                            samples=[db_sample])
