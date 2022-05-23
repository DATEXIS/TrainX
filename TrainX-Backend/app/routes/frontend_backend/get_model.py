import tempfile
import base64
import os
import tarfile
import tempfile
from typing import List, Union

from app.db_models.jobcontainer import db_JobContainer
from app.db_models.mljob import db_MLJob
from app.db_models.model import db_Model
from app.providers.model import ModelProvider
from flask import send_file

from . import frontend


@frontend.route('/session/<session_id>/model', methods=['GET'])
def get_model(session_id):
    """ Returns the last used model of the session"""
    # first get the most recent model
    model_id = db_Model.query.\
            join(db_MLJob).\
            filter(db_Model.job_id == db_MLJob.uid).\
            join(db_JobContainer).\
            filter(db_MLJob.container_id == db_JobContainer.uid).\
            filter(db_JobContainer.session_id == session_id).\
            order_by(db_Model.edited.desc()).first().uid

    MP = ModelProvider()
    model = MP.get(model_id)

    # split the binary and wrap both models(b64 encoded and 
    # separated using a ',')
    ner, nel = model['binary'].split(',', 1)

    ner_wrapper = B64TarWrapper("ner wrapper", ner)
    nel_wrapper = B64TarWrapper("nel wrapper", nel)

    try:
        os.mkdir("./tmp")
        os.mkdir("./tmp/ner")
        os.mkdir("./tmp/nel")
    except FileExistsError:
        pass

    ner_dir = ner_wrapper.get_extract("./tmp/ner")
    nel_dir = nel_wrapper.get_extract("./tmp/nel")

    with open("/tmp/archive.tar.gz", "w") as f:
        f.write("")

    with tarfile.open("/tmp/archive.tar.gz", mode='w:gz') as tar:
        tar.add(ner_dir, arcname="ner")
        tar.add(nel_dir, arcname="nel")

    try:
        return send_file("/tmp/archive.tar.gz", as_attachment=True, attachment_filename='models.tar.gz')
    except FileNotFoundError:
        abort(404)


class B64TarWrapper:

    def __init__(self, identifier: str, tar_base64: str):
        self.identifier: str = identifier
        self.tar_base64: str = tar_base64

    @classmethod
    def from_files(cls, paths: List[str], identifier: Union[str, None] = None):
        tar_file = tempfile.mktemp()
        with tarfile.open(tar_file, 'x') as tar:
            for path in paths:
                tar.add(path, arcname=os.path.basename(path))
        with open(tar_file, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        return cls(identifier=identifier, tar_base64=encoded)

    def get_extract(self, directory: Union[str, None] = None) -> str:
        """
        Extracts the content into a temporary directory and returns the path as string
        :param directory: If given, extraction will take place in this directory
        :return: Path as string
        """
        temp_tar_file = tempfile.NamedTemporaryFile()
        with open(temp_tar_file.name, 'wb') as f:
            f.write(base64.b64decode(self.tar_base64))

        if directory is None:
            directory = tempfile.mkdtemp()

        with tarfile.open(temp_tar_file.name, 'r') as tar:
            for member in tar.getmembers():
                tar.extract(member, directory)

        return directory

    def get_base64_str(self) -> str:
        return self.tar_base64

