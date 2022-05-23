import json

from app.db_models.session import db_Session
from flask import Response

from . import frontend


@frontend.route('/sessions', methods=['GET'])
# returns a list of sessions
def get_sessions():
    """Returns a dictionary which maps all sessions in the database
       to {uid : {title, description}, uid : ...} """
    session_list = db_Session.query.all()
    if len(session_list) == 0:
        return Response(status=404)
    else:
        res = dict()
        for session in session_list:
            session_res = dict()
            session_res['title'] = session.title
            session_res['description'] = session.description
            res[session.uid] = session_res

        res = json.dumps(res)
        return res
