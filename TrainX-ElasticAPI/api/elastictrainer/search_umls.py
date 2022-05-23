import json
from typing import List

import elasticsearch

from . import to_output, create_query


class SearchUmls:

    def __init__(self, ess, q: str, lang: str, limit=50):
        self.text = q.capitalize()
        self.language = lang
        self.limit = limit
        self.index = ess.index
        self.ess = ess

    def search(self) -> List:
        try:
            query = create_query.create_umls_query(self.text, self.language, self.limit)
            res = self.ess.search(query)

            if 'Error' in res:
                res['Message'] = 'Probably no dataset was loaded.'
                json_respond = json.dumps(res, indent=4, sort_keys=True)
                return json_respond

            else:
                hits = res['hits']['hits'].__len__()
                output = []
                for hit in range(0, hits):
                    results = res['hits']['hits'][hit]['_source']
                    output.append(to_output.from_texoo(results))
                json_respond = json.dumps(output, indent=4, sort_keys=True)
                return json_respond

        except elasticsearch.SerializationError:
            return {'Error': 'SerializationError, please send Request again'}

    if __name__ == '__main__':
        __init__()
