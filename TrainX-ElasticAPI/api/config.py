import os
from typing import Dict


def helper() -> Dict[str, str]:
    config = {
        'index': os.environ.get('INDEX', '').lower(),
        'import_file': os.environ.get('IMPORT_FILE', ''),
        'es_host': os.environ.get('ES_HOST', 'localhost'),
    }
    return config
