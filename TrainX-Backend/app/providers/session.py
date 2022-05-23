from app import db
from app.db_models.session import db_Session
from app.models.session import Session
from app.providers.jobcontainer import JobcontainerProvider
from app.routes.responses import Standard404ErrorResponse


class SessionProvider(object):
    # maps a db_Session to a Session object
    def mapper(self, db_Session):
        if not db_Session:
            return Standard404ErrorResponse()
        containers = self.getContainers(db_Session)
        return Session( title=db_Session.title,
                        description=db_Session.description,
                        jobs=containers,
                        session_id=db_Session.uid,
                        )

    # returns linked JobContainers as a list
    def getContainers(self, db_Session):
        JP = JobcontainerProvider()
        containers = []
        for db_container in db_Session.jobs:
            container = JP.mapper(db_container)
            containers.append(container)
        return containers

    # querys and returns a Session object
    def get(self, id, simplified: bool = False):
        db_session: db_Session = db_Session.query.get(id)
        if simplified:
            db_session.jobs = []
            db_session.datasets = []
        return self.mapper(db_session).to_json()

    # creates a db_Session object and posts it to the databank
    def post(self, session_json):
        db_session = db_Session(title=session_json.get('title'),
                                description=session_json.get('description'))
        db.session.add(db_session)
        db.session.commit()
        db_session = db_Session.query.order_by(db_Session.uid.desc()).first()

        JP = JobcontainerProvider()

        for jobcontainer_json in session_json.get('jobs', []):
            JP.post(jobcontainer_json, db_session)
