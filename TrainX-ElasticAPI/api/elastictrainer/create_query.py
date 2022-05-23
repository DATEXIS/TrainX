from typing import Dict

def create_umls_query(text, language, limit) -> Dict[str, str]:
        query = {
            "from": 0, "size": limit,
            "query": {
                "bool": {
                    "should": [
                        { "match": { "title": text }},
                        { "match": { "id": text }}
                    ],
                    "minimum_should_match": 1, 
                    "filter": [
                        { "term":  { "language": language }}
                    ]
                }
            }
        }
        return query


def create_cui_query(cui, fields) -> Dict[str, str]:
        query = {
            "query": {
                "query_string": {
                    "query": cui,
                    "fields": [fields]
                }
            }
        }
        return query
