from typing import Dict

def from_texoo(texoo: dict) -> Dict[str, str]:
    umls = {
        "cui": texoo['id'], 
        "definitions": texoo['text'], 
        "names": {
            texoo['language']: {
                "all": 
                    texoo['title']
            }
        }, 
        "semantic_type": {
            "TUI": "", 
            "name": texoo['type']
        }
    }
    return umls   