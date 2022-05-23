from app import db
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String


class db_Model(db.Model):
    __tablename__ = "model"

    job_id = Column(Integer, ForeignKey('mljob.uid'))
    uid = Column(Integer, primary_key=True)
    path = Column(String)
    edited = Column(DateTime)
