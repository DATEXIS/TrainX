import json

from app import db
from app.db_models.annotation import db_Annotation
from app.db_models.mention_annotation import db_MentionAnnotation
from app.db_models.named_entity_annotation import db_NamedEntityAnnotation
from app.models.annotation import Annotation
from app.models.mention_annotation import MentionAnnotation
from app.models.named_entity_annotation import NamedEntityAnnotation
from app.routes.responses import Standard404ErrorResponse


class AnnotationProvider(object):
    """ maps a db_Annotation obj to a Annotation obj """

    def mapper(self, db_Annotation):
        if not db_Annotation:
            return None

        if db_Annotation.confidence is None:
            db_Annotation.confidence = 0

        if db_Annotation.annotation_type == 'SimpleAnnotation':
            return Annotation(  uid=db_Annotation.uid,
                                begin=db_Annotation.begin,
                                length=db_Annotation.length,
                                text=db_Annotation.text,
                                source=db_Annotation.source,
                                confidence=float(db_Annotation.confidence))
        if db_Annotation.annotation_type == 'MentionAnnotation':
            return MentionAnnotation(uid=db_Annotation.uid,
                                begin=db_Annotation.begin,
                                length=db_Annotation.length,
                                text=db_Annotation.text,
                                source=db_Annotation.source,
                                confidence=float(db_Annotation.confidence),
                                type=db_Annotation.type,
                                refId=db_Annotation.refId)
        if db_Annotation.annotation_type == 'NamedEntityAnnotation':
            return NamedEntityAnnotation(uid=db_Annotation.uid,
                                begin=db_Annotation.begin,
                                length=db_Annotation.length,
                                text=db_Annotation.text,
                                source=db_Annotation.source,
                                confidence=float(db_Annotation.confidence),
                                refId=db_Annotation.refId)

    def get(self, uid):
        """querys and returns an Annotation obj by id"""
        db_annotation = db_Annotation.query.get(uid)
        if not db_annotation:
            Standard404ErrorResponse()
        annotation = self.mapper(db_annotation)
        return annotation.to_json()

    def post(self, annotation_json, db_document=None):
        """ writes an Annotation json to the db """
        if annotation_json['class'] == 'MentionAnnotation':
            db_annotation = db_MentionAnnotation(
                begin=annotation_json['begin'],
                confidence=annotation_json['confidence'],
                length=annotation_json['length'],
                text=annotation_json['text'],
                source=annotation_json['source'],
                type=annotation_json['type'],
                refId=annotation_json.get('refId', None ))

        elif annotation_json['class'] == 'NamedEntityAnnotation':
            db_annotation = db_NamedEntityAnnotation(
                begin=annotation_json['begin'],
                confidence=annotation_json['confidence'],
                length=annotation_json['length'],
                text=annotation_json['text'],
                source=annotation_json['source'],
                refId=annotation_json.get('refId', None))

        db_annotation.document = db_document
        db.session.add(db_annotation)
        db.session.commit()


    def update(self, annotation_json):
        """updates as existing db_Annotation obj"""
        annotation_json = json.loads(annotation_json)
        uid = annotation_json['uid']
        db_annotation = db_Annotation.query.get(uid)

        if(db_annotation.__mapper_args__.
           get('polymorphic_identity') == 'MentionAnnotation'):
            # update mention annotation
               db_annotation.begin = annotation_json['begin'],
               db_annotation.length = annotation_json['length'],
               db_annotation.text = annotation_json['text'],
               db_annotation.source = annotation_json['source'],
               db_annotation.confidence = annotation_json['confidence'],
               db_annotation.type = annotation_json['type'],
               db_annotation.refId = annotation_json['refId']

        if(db_annotation.__mapper_args__.
           get('polymorphic_identity') == 'NamedEntityAnnotation'):
            # update mention annotation
               db_annotation.begin=annotation_json['begin'],
               db_annotation.length=annotation_json['length'],
               db_annotation.text=annotation_json['text'],
               db_annotation.source=annotation_json['source'],
               db_annotation.confidence=annotation_json['confidence'],
               db_annotation.refId=annotation_json['refId']

        db.session.commit()
