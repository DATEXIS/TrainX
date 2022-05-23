from app import db
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship


class db_Document(db.Model):
    __tablename__ = "document"

    id = Column(String)
    uid = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String)
    begin = Column(Integer)
    length = Column(Integer)
    title = Column(String)
    type = Column(String)
    text = Column(Text)
    dataset_id = Column(Integer, ForeignKey('dataset.uid'))
    avg_confidence = Column(Integer)

    annotations = relationship('db_Annotation', backref='document',
                               lazy='dynamic', cascade='all, delete-orphan')
