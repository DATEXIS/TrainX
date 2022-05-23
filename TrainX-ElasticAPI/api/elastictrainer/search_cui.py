import json
from typing import List

import elasticsearch

from . import to_output, create_query


class SearchCui:

    def __init__(self, ess, cui: str):
        self.cui = cui
        self.index = ess.index
        self.ess = ess


    def search(self) -> List:
        try:
            query = create_query.create_cui_query(self.cui, "id")
            res = self.ess.search(query)
            hits = res['hits']['hits'].__len__()
            
            output = []

            for hit in range(0, hits):
                source = res['hits']['hits'][hit]['_source']
                cui = source['id']
                if cui == self.cui:
                    output.append(to_output.from_texoo(source))
                    break
                else:
                    output.append({'info': 'no results found for ' + self.cui})

            json_respond = json.dumps(output, indent=4, sort_keys=True)
            return json_respond

        except elasticsearch.SerializationError:
            return {'Error' : 'SerializationError, please send Request again'}


    if __name__ == '__main__':
        __init__()
