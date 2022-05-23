from app import db
from sqlalchemy import Column, Integer


class db_NERModel(db.Model):
    __tablename__ = "nermodel"

    uid = Column(Integer, primary_key=True)
