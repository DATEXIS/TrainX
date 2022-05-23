import unittest
from api.app import app, Helpers, parse_url_parameter
from elasticmock import elasticmock
from api.elastictrainer.elasticservice import ElasticsearchService
from api import config
try:
    from .test_helper import TestHelper
except ModuleNotFoundError:
    from test_helper import TestHelper


class FlaskTestCase(unittest.TestCase):

    @elasticmock
    def setUp(self):
        self.config = config.helper()
        self.ess = ElasticsearchService(self.config['index'], self.config['import_file'], self.config['es_host'])
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertTrue(app.testing)
        self.assertFalse(app.debug)
        self.helper = Helpers
        self.helper.ess = self.ess
        self.test_helper = TestHelper()

    def tearDown(self):
        pass

    def test_check_test_endpoint(self):
        response = self.app.get('/test')
        self.assertEqual(response.status_code, 200)

    @elasticmock
    def test_cui_endpoint(self):
        self.test_helper.bulk_test_doc(self.ess)
        response = self.app.get('/cui/?cui=C0001924')
        self.assertEqual(response.status_code, 200)

    @elasticmock
    def test_query_endpoint_all_params_given(self):
        self.test_helper.bulk_test_doc(self.ess)
        response = self.app.get('/?query=beer&language=en&limit=10')
        self.assertEqual(response.status_code, 200)

    def test_query_endpoint_missing_language(self):
        response = self.app.get('/?query=beer')
        self.assertEqual(response.status_code, 400)

    def test_query_endpoint_missing_query(self):
        response = self.app.get('/?language=en')
        self.assertEqual(response.status_code, 400)

    def test_query_endpoint_not_supported_language(self):
        response = self.app.get('/?query=beer&language=beer')
        self.assertEqual(response.status_code, 400)

    def test_cui_missing(self):
        response = self.app.get('/cui/')
        self.assertEqual(response.status_code, 400)

    def test_parse_url_parameter(self):
        expected_string = 'süß-säuerliches-sößchen'
        url_parameter = 's%C3%BC%C3%9F-s%C3%A4uerliches-s%C3%B6%C3%9Fchen'
        self.assertEqual(parse_url_parameter(url_parameter), expected_string)


if __name__ == '__main__':
    unittest.main()
