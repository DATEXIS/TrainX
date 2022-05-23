from sqlalchemy import Column, String, Integer, ForeignKey

from .annotation import db_Annotation


class db_MentionAnnotation(db_Annotation):
    __tablename__ = 'mention_annotation'
    uid = Column(Integer, ForeignKey('annotation.uid', ondelete='CASCADE'), primary_key=True)
    type = Column(String)
    refId = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'MentionAnnotation'
    }
