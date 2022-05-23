from app import db
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class db_MLJob(db.Model):
    __tablename__ = "mljob"

    uid = Column(Integer, primary_key=True)
    status = Column(String)
    type = Column(String)
    container_id = Column(Integer, ForeignKey('jobcontainer.uid'))

    dataset = relationship("db_Dataset", uselist=False, backref="mljob")
    model = relationship("db_Model", uselist=False, backref="mljob")
