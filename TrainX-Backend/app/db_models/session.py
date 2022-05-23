from app import db
from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship


class db_Session(db.Model):
    __tablename__ = "session"

    uid = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    jobs = relationship('db_JobContainer', backref='session')
    datasets = relationship("db_Dataset", backref="session")
