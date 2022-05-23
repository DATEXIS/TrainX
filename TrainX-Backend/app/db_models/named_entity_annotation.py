from sqlalchemy import Column, String, Integer, ForeignKey

from .annotation import db_Annotation


class db_NamedEntityAnnotation(db_Annotation):
    __tablename__ = 'named_entity_annotation'
    uid = Column(Integer, ForeignKey('annotation.uid', ondelete='CASCADE'), primary_key=True)
    refId = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'NamedEntityAnnotation'
    }
