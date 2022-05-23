from app import db
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class db_Dataset(db.Model):
    __tablename__ = "dataset"

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    language = Column(String)
    session_id = Column(Integer, ForeignKey('session.uid'))
    mljob_id = Column(Integer, ForeignKey('mljob.uid'))

    documents = relationship('db_Document', backref='dataset', lazy='dynamic')
