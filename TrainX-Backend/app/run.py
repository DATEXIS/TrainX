import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


def create_app():
    # initialize app
    app = Flask(__name__)

    if 'TESTING' in os.environ:
        app.config['DEBUG'] = os.environ['DEBUG']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    else:
        app.config['DEBUG'] = os.environ['DEBUG']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
            user=os.environ['DB_USER'],
            passwd=os.environ['DB_PASS'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            db=os.environ['DB_NAME'])

    db = SQLAlchemy(app)
    return (app, db)


def register_blueprints(app):
    url_prefix = os.environ['URL_PREFIX']

    # import the blueprint for frontend_backend communication
    from app.routes.frontend_backend import frontend
    # import the blueprint for backend ml_component communication
    from app.routes.backend_ml import ml_component

    # register blueprints
    app.register_blueprint(frontend, url_prefix=url_prefix)
    app.register_blueprint(ml_component, url_prefix=url_prefix)
    CORS(app)

