from . import frontend


@frontend.route('/session/<session_id>/metric', methods=['GET'])
# returns the metric of the session
def get_metric(session_id):
    resp = 'OK'
    return resp
