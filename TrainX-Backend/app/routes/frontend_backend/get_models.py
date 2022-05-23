from . import frontend


@frontend.route('/session/<session_id>/models', methods=['GET'])
def get_models(session_id):
    """Returns list of models as json"""
    """Not used"""
    pass
