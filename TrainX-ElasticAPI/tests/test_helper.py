import json
from api.elastictrainer.elasticservice import ElasticsearchService


class TestHelper:
    test_doc = {
        "begin": 0,
        "length": 571,
        "text": "A family of globular proteins found in many plant and animal tissues that tend to bind a wide variety of ligands. Albumin is the main protein in blood plasma. Low serum levels occur in conditions associated with malnutrition, inflammation and liver and kidney diseases. Water-soluble proteins found in egg whites, blood, lymph, and other tissues and fluids. They coagulate upon heating. family of globular proteins found in many plant and animal tissues that tend to bind a wide variety of ligands. A type of protein found in blood, egg white, milk, and other substances.",
        "id": "C0001924",
        "title": ["albumins", "Albumins", "Albumin", "albumin", "ALBUMIN"],
        "language": "en",
        "type": "Biologically Active Substance",
        "annotations": [],
        "class": "Document"
    }

    def bulk_test_doc(self, ess: ElasticsearchService):
        action = json.dumps({'index': {'_index': ess.index, '_type': 'doc'}})
        body = [action, json.dumps(self.test_doc, default=str)]
        body = '\n'.join(body)
        return ess.bulkData(body)
