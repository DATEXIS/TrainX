class NERModel(object):
    def __init__(self, **kwargs):
        self.uid: int = kwargs.get('uid', None)
        self.model = kwargs.get('model')
