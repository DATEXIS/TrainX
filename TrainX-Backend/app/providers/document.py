import json

from app import db
from app.db_models.document import db_Document
from app.models.document import Document
from app.providers.annotation import AnnotationProvider
from app.routes.responses import Standard404ErrorResponse


class DocumentProvider(object):
    # maps a db_Document obj to a Document obj
    def mapper(self, db_Document):
        if not db_Document:
            return None
        annotations = self.getAnnotations(db_Document)

        return Document(uid=db_Document.uid,
                        begin=db_Document.begin,
                        length=db_Document.length,
                        text=db_Document.text,
                        id=db_Document.id,
                        title=db_Document.title,
                        language=db_Document.language,
                        type=db_Document.type,
                        annotations=annotations) #We don't have a class for sentences yet

    # returns the Annotation objs assoziated with the db_Document as a list
    def getAnnotations(self, db_document):
        db_annotations  = db_document.annotations
        annotations     = []
        AP              = AnnotationProvider()
        for db_annotation in db_annotations:
            annotation      = AP.mapper(db_annotation)
            annotations.append(annotation)
        return annotations

    # querys and returns a Document obj by id as json
    def get(self, id):
        db_document     = db_Document.query.get(id)
        if not db_document:
            Standard404ErrorResponse()
        document = self.mapper(db_document)
        document_json = document.to_json()
        return document_json

    # writes a Document obj to the db and links it to a dataset obj if a dataset is provided
    # also calculates the average confidence for the Document
    def post(self, json_document, db_dataset=None):
        db_document = db_Document(
                                    id=json_document['id'],
                                    language=json_document['language'],
                                    begin=json_document['begin'],
                                    length=json_document['length'],
                                    title=json_document['title'],
                                    type=json_document['type'],
                                    avg_confidence = 0,
                                    text=json_document['text'])
        db_document.dataset = db_dataset
        db.session.add(db_document)
        db.session.commit()

        annotation_count = 0
        confidence_sum = 0
        if json_document['annotations']:
            AP = AnnotationProvider()
            for annotation in json_document['annotations']:
                # save annotation to db
                AP.post(annotation, db_document)
                # calculate the avg. confidence
                annotation_count = annotation_count + 1
                confidence_sum = confidence_sum + annotation['confidence']
            db_document.avg_confidence = confidence_sum / annotation_count
            db.session.commit()

    def update(self, document_json):
        document_json = json.loads(document_json)
        uid = document_json['uid']
        db_document = db_Document.query.get(uid)

        db_document.id = document_json['id']
        db_document.language = document_json['language']
        db_document.begin = document_json['begin']
        db_document.length = document_json['length']
        db_document.title = document_json['title']
        db_document.type = document_json['type']
        db_document.text = document_json['text']

        db.session.commit()

        for annotation_json in document_json['annotations']:
            AP = AnnotationProvider()
            AP.update(json.dumps(annotation_json))
