import os

from app import db
from sqlalchemy import Column, String, Integer, Numeric, ForeignKey


class db_Annotation(db.Model):
    __tablename__ = "annotation"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    begin = Column(Integer)
    length = Column(Integer)
    text = Column(String)
    source = Column(String)
    if 'TESTING' in os.environ:
        confidence = Column(Integer)
    else:
        confidence = Column(Numeric)
    document_id = Column(Integer, ForeignKey('document.uid'))
    annotation_type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'SimpleAnnotation',
        'polymorphic_on': annotation_type
    }
