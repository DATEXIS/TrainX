from app import db
from app.db_models.session import db_Session
from app.providers.session import SessionProvider
from app.routes.responses import Standard200Response
from flask import request

from . import frontend


@frontend.route('/session', methods=['POST'])
# add a new session to list
# only accepts .json
def post_session():
    req_data = request.get_json()
    SP = SessionProvider()
    SP.post(req_data)

    new_session_id = db.session.query(db_Session).\
            order_by(db_Session.uid.desc()).first().uid
    return Standard200Response(SP.get(new_session_id))
