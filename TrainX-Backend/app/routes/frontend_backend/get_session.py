from app.providers.session import SessionProvider

from . import frontend


@frontend.route('/session/<session_id>', methods=['GET'])
# returns a session by its ID
def get_session(session_id):
    SP = SessionProvider()
    return SP.get(session_id, simplified=True)
