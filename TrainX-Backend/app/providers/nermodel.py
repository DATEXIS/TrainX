from app import db
from app.db_models.nermodel import db_NERModel
from app.models.nermodel import NERModel


class NermodelProvider(object):
    def mapper(self, db_NERModel):
        return NERModel(db_NERModel.model, db_NERModel.id)

    def get(self, id):
        db_nermodel = db_NERModel.query.get(id)
        return self.mapper(db_nermodel)

    def post(self, nermodel):
        db_nermodel = db_NERModel(model=nermodel.model)
        db.session.add(db_nermodel)
        db.session.commit()
