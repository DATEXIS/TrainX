# ElasticTraiNER

## Run tests 
```
python3 -m unittest -v tests/elasticsearch_test.py
python3 -m unittest -v tests/api_test.py
```

## Parameters to change
in **docker-compose**:

- volumes: **_/Users/Studium/DATEXIS/Data/TraiNER-ES_**: -> where import file is located

depends on run only (**docker-compose**) or in TraiNER-Integration (change in **config/elastic-api.env**)

- IMPORT_FILE=UMLS2017AA_en_1k_texoo.json (file has to be json or zipped json in **texoo** format. Anyways, file must be declared as .json, even if it's zipped).


## Import file 
for format details see **parameters to change** IMPORT_FILE

f.g.: 
```
{
   "name":"UMLS2017AA-EN-1k",
   "language":"en",
   "documents":[
      {
         "begin":0,
         "length":571,
         "text":"A family of globular proteins found in many plant and animal tissues that tend to bind a wide variety of ligands. Albumin is the main protein in blood plasma. Low serum levels occur in conditions associated with malnutrition, inflammation and liver and kidney diseases. Water-soluble proteins found in egg whites, blood, lymph, and other tissues and fluids. They coagulate upon heating. family of globular proteins found in many plant and animal tissues that tend to bind a wide variety of ligands. A type of protein found in blood, egg white, milk, and other substances.",
         "id":"C0001924",
         "title":"\"albumins\",\"Albumins\",\"Albumin\",\"albumin\",\"ALBUMIN\"\n",
         "language":"en",
         "type":"Biologically Active Substance",
         "annotations":[],
         "class":"Document"
      }, 
      ...
    ],
    "queries":[]
}
```
UMLS objects stored in documents, where **id** is CUI, **title** is entity (if multiple names given, seperated with comma in csv style) and in annotations **sectionHeading** _or_ **sectionLabel** is the name of the sematic type.
<br/>

# Usage

## 1. Search for entity in specific language
Flask app that receives a query, a language and optional a result limit, searches with the given parameters in elasticsearch and returns a JSON-result.

Scores hits with given query. <br/>
Filtering results for given languange. Possible languages: _en_ for englisch, and _de_ for german. <br/>
Default maximum limit is _50_.

## Request example
GET
http://localhost:3000/?query=albumin&language=en&limit=1 </br>

curl -X GET "http://localhost:3000/?query=albumin&language=en&limit=1" -H "accept: application/json"

## Respond example
```yaml
[
    {
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
]  
```
<br/>

## 2. Search for specific CUI
Flask app that receives a cui and searches with the given parameter in elasticsearch and returns a JSON-result.

Scores hits with given cui. <br/>

## Request example
GET
http://localhost:3000/cui/?cui=C0000005 </br>

curl -X GET "http://localhost:3000/cui/?cui=C0000005" -H "accept: application/json"

## Respond example 
```yaml
[
    {
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
]
```
