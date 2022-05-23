from app import app, db
from waitress import serve

# All the following imports are just there to use in the flask shell
from app.db_models.annotation import db_Annotation
from app.db_models.dataset import db_Dataset
from app.db_models.document import db_Document
from app.db_models.jobcontainer import db_JobContainer
from app.db_models.mention_annotation import db_MentionAnnotation
from app.db_models.mljob import db_MLJob
from app.db_models.model import db_Model
from app.db_models.named_entity_annotation import db_NamedEntityAnnotation
from app.db_models.nermodel import db_NERModel
from app.db_models.session import db_Session

from app.models.annotation import Annotation
from app.models.dataset import Dataset
from app.models.document import Document
from app.models.jobcontainer import JobContainer
from app.models.mention_annotation import MentionAnnotation
from app.models.mljob import MLJob
from app.models.model import Model
from app.models.named_entity_annotation import NamedEntityAnnotation
from app.models.nermodel import NERModel
from app.models.session import Session

from app.providers.annotation import AnnotationProvider
from app.providers.dataset import DatasetProvider
from app.providers.document import DocumentProvider
from app.providers.jobcontainer import JobcontainerProvider
from app.providers.mljob import MljobProvider
from app.providers.model import ModelProvider
from app.providers.nermodel import NermodelProvider
from app.providers.session import SessionProvider


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'db_Session': db_Session,
            'db_Annotation': db_Annotation,
            'db_MentionAnnotation': db_MentionAnnotation,
            'db_NamedEntityAnnotation': db_NamedEntityAnnotation,
            'db_JobContainer': db_JobContainer,
            'db_MLJob': db_MLJob,
            'db_Model': db_Model,
            'db_Dataset': db_Dataset,
            'db_NERModel': db_NERModel,
            'db_Document': db_Document,
            'SessionProvider': SessionProvider,
            'AnnotationProvider': AnnotationProvider,
            'JobcontainerProvider': JobcontainerProvider,
            'MljobProvider': MljobProvider,
            'ModelProvider': ModelProvider,
            'DatasetProvider': DatasetProvider,
            'DocumentProvider': DocumentProvider,
            'Session': Session,
            'Annotation': Annotation,
            'MentionAnnotation': MentionAnnotation,
            'NamedEntityAnnotation': NamedEntityAnnotation,
            'JobContainer': JobContainer,
            'MLJob': MLJob,
            'Model': Model,
            'Dataset': Dataset,
            'NERModel': NERModel,
            'Document': Document}

# deploy app using waitress serve

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000, max_request_body_size=16*1024*1024*1024)
