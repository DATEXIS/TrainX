import os
import unittest
from .testdata import TestData

os.environ['TESTING'] = 'True'
os.environ['DEBUG'] = 'False'
os.environ['URL_PREFIX'] = '/testing'

from .provider_tests.annotation import AnnotationProviderTest
from .provider_tests.dataset import DatasetProviderTest
from .provider_tests.document import DocumentProviderTest
from .provider_tests.jobcontainer import JobcontainerProviderTest
from .provider_tests.mljob import MljobProviderTest
from .provider_tests.model import ModelProviderTest
from .provider_tests.sample import SampleProviderTest
from .provider_tests.session import SessionProviderTest
from .endpoint_tests.get_endpoints import Test_get_endpoints

def suite():
    suite = unittest.TestSuite()
    suite.addTest(AnnotationProviderTest('test_annotation_provider'))
    suite.addTest(DatasetProviderTest('test_dataset_provider'))
    suite.addTest(DocumentProviderTest('test_document_provider'))
    suite.addTest(JobcontainerProvider('test_jobcontainer_provider'))
    suite.addTest(MljobProviderTest('test_mljob_provider'))
    suite.addTest(ModelProviderTest('test_model_provider'))
    suite.addTest(SampleProviderTest('test_sample_provider'))
    suite.addTest(SessionProviderTest('test_session_provider'))
    suite.addTest(Test_get_endpoints('test_the_get_endpoints'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
