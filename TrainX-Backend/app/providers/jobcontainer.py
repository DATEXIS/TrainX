import datetime

from app import db
from app.db_models.jobcontainer import db_JobContainer
from app.models.jobcontainer import JobContainer
from app.providers.mljob import MljobProvider


class JobcontainerProvider(object):
    # maps a db_JobContainer obj to a JobContainer
    def mapper(self, db_JobContainer):
        if not db_JobContainer:
            return None

        mljob = self.getJob(db_JobContainer)
        return JobContainer(callbackUrl=db_JobContainer.callbackUrl,
                            timestamp=db_JobContainer.timestamp,
                            mljob=mljob,
                            uid=db_JobContainer.uid,
                            session_id=db_JobContainer.session_id)

    # returns the MLJob assoziated with the jobcontainer
    def getJob(self, db_Jobcontainer):
        db_jobcontainer = db_Jobcontainer.job
        MP = MljobProvider()
        return MP.mapper(db_jobcontainer)

    # querys and returns a JobContainer obj by id
    def get(self, uid):
        db_jobcontainer = db_JobContainer.query.get(uid)
        return self.mapper(db_jobcontainer).to_json()

    def get_last(self):
        db_jobcontainer = db_JobContainer.query.\
                order_by(db_JobContainer.uid.desc()).first()
        return self.mapper(db_jobcontainer).to_json()

    # writes a JobContainer obj to the db and links it with a Session obj
    def post(self, jobcontainer_json, session=None):
        db_jobcontainer = db_JobContainer(  callbackUrl=jobcontainer_json['callbackUrl'],
                                            timestamp=jobcontainer_json.get('timestamp', datetime.datetime.utcnow()),
                                            session=session)
        db.session.add(db_jobcontainer)
        db.session.commit()

        if jobcontainer_json['mljob']:
            db_jobcontainer = db_JobContainer.query.order_by(db_JobContainer.uid.desc()).first()
            MP = MljobProvider()
            MP.post(jobcontainer_json.get('mljob'), db_jobcontainer)

    def update(self, jobcontainer_json):
        """Update an existing JobContainer after a job was completed"""

        uid = jobcontainer_json.get('uid')
        db_jobcontainer = db_JobContainer.query.get(uid)

        db_jobcontainer.callbackUrl = jobcontainer_json.get('callbackUrl')
        db_jobcontainer.timestamp = datetime.datetime.utcnow()
        db.session.commit()

        if 'mljob' in jobcontainer_json:
            mljob_json = jobcontainer_json.get('mljob')
            MP = MljobProvider()
            if db_jobcontainer.job:
                MP.update(mljob_json)
            else:
                MP.post(mljob_json, db_jobcontainer)

