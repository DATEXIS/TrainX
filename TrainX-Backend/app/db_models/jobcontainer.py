from app import db
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class db_JobContainer(db.Model):
    __tablename__ = "jobcontainer"

    session_id = Column(Integer, ForeignKey('session.uid'))
    uid = Column(Integer, primary_key=True)
    callbackUrl = Column(String)
    timestamp = Column(DateTime, index=True)
    job = relationship("db_MLJob", uselist=False, backref="jobcontainer")
