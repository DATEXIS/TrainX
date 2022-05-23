import urllib.parse

from flask import Flask, request, abort
from flask_cors import CORS
from waitress import serve

try:
    from elastictrainer.search_cui import SearchCui
    from elastictrainer.search_umls import SearchUmls
    from elastictrainer.elasticservice import ElasticsearchService
    import config
except Exception: #ImportError
    from api.elastictrainer.search_cui import SearchCui
    from api.elastictrainer.search_umls import SearchUmls
    from api.elastictrainer.elasticservice import ElasticsearchService
    from api import config


def parse_url_parameter(param: str) -> str:
    return urllib.parse.unquote(param)


class Helpers:
    supported_languages = ['de', 'en']
    conf = config.helper()
    ess = ElasticsearchService(conf['index'], conf['import_file'], conf['es_host'])

    def __init__(self):
        if self.conf['index']:
            self.ess.loadInElasticSearch()
        else:
            print('No index name giving. Data will not be loaded!')


app = Flask(__name__)
CORS(app, support_credentials=True)
helper = Helpers()


@app.route('/', methods=['GET'])
def get_umls():
    query = request.args.get('query', type=str)
    language = request.args.get('language', type=str)
    limit = request.args.get('limit', default=50, type=int)
    if query and language is not None:
        if language in helper.supported_languages:
            query = parse_url_parameter(query)
            results = SearchUmls(helper.ess, query, language, limit).search()
            return results
        else:
            abort(400)
    else:
        abort(400)


@app.route('/cui/', methods=['GET'])
def get_cui():
    cui = request.args.get('cui', type=str)
    if cui is not None:
        cui = parse_url_parameter(cui)
        results = SearchCui(helper.ess, cui).search()
        return results
    else:
        abort(400)


@app.route('/test', methods=['GET'])
def test():
    return 'test was successful'


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port="3000")


