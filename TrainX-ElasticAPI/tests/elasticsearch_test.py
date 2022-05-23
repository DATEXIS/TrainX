import unittest
from elasticmock import elasticmock
from api.elastictrainer import create_query, to_output
from api.elastictrainer.importJson import csv2names, validImportDocument
from api.elastictrainer.elasticservice import ElasticsearchService
from api import config
try:
    from .test_helper import TestHelper
except ModuleNotFoundError:
    from test_helper import TestHelper


class ElasticsearchTestCase(unittest.TestCase):

    @elasticmock
    def setUp(self):
        self.config = config.helper()
        self.ess = ElasticsearchService(self.config['index'], self.config['import_file'], self.config['es_host'])
        self.es = self.ess.es
        self.ess.index = 'test-index'
        self.test_helper = TestHelper()

    def tearDown(self):
        pass

    # NOT WORKING because exception with elasticmock bulk
    @elasticmock
    def test_write_and_read_obj(self):
        resp = self.test_helper.bulk_test_doc(self.ess)
        items = resp.get('items')
        index = items[0].get('index')

        self.assertEqual('doc', index.get('_type'))
        self.assertEqual(self.ess.index, index.get('_index'))
        self.assertEqual('created', index.get('result'))
        self.assertEqual(201, index.get('status'))

    @elasticmock
    def test_cui_search_result(self):
        self.test_helper.bulk_test_doc(self.ess)
        search_cui = create_query.create_cui_query(self.test_helper.test_doc['id'], 'id')
        resp = self.ess.search(search_cui)
        cui = resp['hits']['hits'][0]['_source']['id']
        self.assertEqual(self.test_helper.test_doc['id'], cui)

    @elasticmock
    def test_query_search_result(self):
        self.test_helper.bulk_test_doc(self.ess)
        search_umls = create_query.create_umls_query('albumin', 'en', 1)
        resp = self.ess.search(search_umls)
        cui = resp['hits']['hits'][0]['_source']['id']
        self.assertEqual(self.test_helper.test_doc['id'], cui)

    @elasticmock
    def test_search_in_none_existing_dataset(self):
        search_umls = create_query.create_umls_query('albumin', 'en', 1)
        resp = self.ess.search(search_umls)
        self.assertEqual('Error' in resp, True)

    @elasticmock
    def test_for_es_connection(self):
        self.assertIsNotNone(self.ess.es)

    # NOT WORKING because can not establish connection to Elasticsearch, which is needed.
    @elasticmock
    def test_check_for_index(self):
        test_index = self.ess.checkIfIndexExists('text-index')
        self.assertEqual(test_index, False)

    @elasticmock
    def test_create_cui_query(self):
        expected_query = {
            "query": {
                "query_string": {
                    "query": 'C0004922',
                    "fields": ['id']
                }
            }
        }
        self.assertEqual(create_query.create_cui_query('C0004922', 'id'), expected_query)

    @elasticmock
    def test_create_umls_query(self):
        expected_query = {
            "from": 0, "size": 10,
            "query": {
                "bool": {
                    "should": [
                        { "match": { "title": 'beer' }},
                        { "match": { "id": 'beer' }}
                    ],
                    "minimum_should_match": 1, 
                    "filter": [
                        {"term": {"language": 'en'}}
                    ]
                }
            }
        }
        self.assertEqual(create_query.create_umls_query('beer', 'en', 10), expected_query)

    @elasticmock
    def test_csv2names(self):
        expected_list = ['Enzyme, 1,4-alpha-Glucan Branching', 'Branching Enzyme, 1,4-alpha-Glucan',
                         '1,4-alpha-Glucan Branching Enzyme', '1,4 alpha Glucan Branching Enzyme',
                         '1,4-Alpha glucan branching enzyme', '1,4-alpha-Glucan branching enzyme']
        test_str = "\"Enzyme, 1,4-alpha-Glucan Branching\",\"Branching Enzyme, 1,4-alpha-Glucan\",\"1,4-alpha-Glucan Branching Enzyme\",\"1,4 alpha Glucan Branching Enzyme\",\"1,4-Alpha glucan branching enzyme\",\"1,4-alpha-Glucan branching enzyme\"\n"
        self.assertEqual(csv2names(test_str), expected_list)

    @elasticmock
    def test_from_texoo_to_umls_output(self):
        texoo_obj = {
            "begin": 0,
            "length": 571,
            "text": "A family of globular proteins found in many plant and animal tissues that tend to bind a wide variety of ligands. Albumin is the main protein in blood plasma. Low serum levels occur in conditions associated with malnutrition, inflammation and liver and kidney diseases. Water-soluble proteins found in egg whites, blood, lymph, and other tissues and fluids. They coagulate upon heating. family of globular proteins found in many plant and animal tissues that tend to bind a wide variety of ligands. A type of protein found in blood, egg white, milk, and other substances.",
            "id": "C0001924",
            "title": "\"albumins\",\"Albumins\",\"Albumin\",\"albumin\",\"ALBUMIN\"\n",
            "language": "en",
            "type": "Biologically Active Substance",
            "annotations": [],
            "class": "Document"
        }
        umls = {
            "cui": "C0001924",
            "definitions": "A family of globular proteins found in many plant and animal tissues that tend to bind a wide variety of ligands. Albumin is the main protein in blood plasma. Low serum levels occur in conditions associated with malnutrition, inflammation and liver and kidney diseases. Water-soluble proteins found in egg whites, blood, lymph, and other tissues and fluids. They coagulate upon heating. family of globular proteins found in many plant and animal tissues that tend to bind a wide variety of ligands. A type of protein found in blood, egg white, milk, and other substances.",
            "names": {
                "en": {
                    "all": [
                        "albumins",
                        "Albumins",
                        "Albumin",
                        "albumin",
                        "ALBUMIN"
                    ]
                }
            },
            "semantic_type": {
                "TUI": "",
                "name": "Biologically Active Substance"
            }
        }
        texoo_obj['title'] = csv2names(texoo_obj['title'])
        self.assertEqual(to_output.from_texoo(texoo_obj), umls)

    @elasticmock
    def test_missing_text_key_in_doc(self):
        doc_with_missing_keys = {
            "begin": 0,
            "length": 571,
            "id": "C0001924",
            "title": "\"albumins\",\"Albumins\",\"Albumin\",\"albumin\",\"ALBUMIN\"\n",
            "language": "en",
            "type": "Biologically Active Substance",
            "annotations": [],
            "class": "Document"
        }
        self.assertFalse(validImportDocument(doc_with_missing_keys))


if __name__ == '__main__':
    unittest.main()
