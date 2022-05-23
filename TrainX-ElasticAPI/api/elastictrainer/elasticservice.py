import json
from typing import Dict, List

import elasticsearch

from .importJson import load


class ElasticsearchService:

    def __init__(self, index: str, import_file: str, es_host: str):
        self.index = index
        self.import_file = import_file
        self.es_host = es_host
        self.es = elasticsearch.Elasticsearch([self.es_host + ':9200'])

    def loadInElasticSearch(self):
        if not self.checkIfIndexExists(self.index):
            load(self)
        else:
            print("Index: '{}' already exists. '{}' will not be loaded. \n".format(self.index, self.import_file))

    def checkIfIndexExists(self, idx: str) -> bool:
        return self.es.indices.exists(idx)  

    def bulkData(self, data: list) -> Dict[str, str]:
        return self.es.bulk(index=self.index, body=data, request_timeout=20)
    
    def search(self, query: dict) -> Dict[str, str]:
        try:
            return self.es.search(index=self.index, body=query)
        except elasticsearch.NotFoundError:
            return {'Error': 'Not Found Error'}

    def genData(self, data: list) -> List[Dict]:
        action = []
        amountDataInOneList = 5000
        action_index = json.dumps({'index': {'_index': self.index}})
        listOfActions = []

        for doc in data:
            body = json.dumps(doc, default=str)
            action.append(action_index)
            action.append(body)
            if len(action) == amountDataInOneList:
                listOfActions.append(action)
                action = []

        if not listOfActions or action:
            listOfActions.append(action)

        return listOfActions
