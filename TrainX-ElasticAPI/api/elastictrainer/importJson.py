import csv
import json
import os
from io import StringIO
from os import listdir
from typing import List

import elasticsearch


def load(ess):
    try:
        os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/src")
        if os.path.isfile("../../../iHaveFailed"+ess.index+".txt"):
            ess.es.indices.delete(index=ess.index, ignore=[400, 404])


        print("Loading {} into elasticsearch... with index {}".format(ess.import_file, ess.index))
        print("all dir and files in \'src\': " + str(listdir(".")))
        file = open(ess.import_file, 'r', encoding='utf-8')

        texoo = json.load(file)
        data = texoo['documents'] 
        for doc in data: 
            doc['title'] = csv2names(doc['title'])
            if not validImportDocument(doc):
                data.remove(doc)
                print('Warning, Document contains missings fields. Therefore it will not be loaded into ElasticSearch!')

        dataList = ess.genData(data)
        uploadSucceeded = True
        for data in dataList: 
            resp = ess.bulkData(data)
            items = resp.get('items')
            for item in items:
                index = item.get('index')
                if index.get('status') is not 201:
                    uploadSucceeded = False
        if uploadSucceeded:
            open("../../../iHaveSuccessfullyFinished" + ess.index + ".txt", "w+")
            print("Loading done")
    
        else:
            open("../../../iHaveFailed"+ess.index+".txt", "w+")
            msg = "Error during upload. %s documents successfully uploaded. \
                            Status: %s.\n"
            raise Exception(msg % (item, "\n".join(index.get('status'))))

        file.close()
        


    except elasticsearch.ConnectionError:
        print("Connection to ElasticSearch failed.")

    except IOError:
        print(os.environ['IMPORT_FILE'], "not found.")



def validImportDocument(doc: dict) -> bool:
    if all(k in doc for k in ('id', 'text', 'language', 'title', 'type')):
        return True
    else:
        return False


def csv2names(csv_str: str) -> List[str]:
    infile = StringIO(csv_str)
    reader = csv.reader(infile, dialect='unix')
    for row in reader:
        return row


