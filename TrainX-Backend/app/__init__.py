from .run import create_app, register_blueprints

# create app and database
app, db = create_app()

# register blueprints
register_blueprints(app)

from .tables import create_tables

# create database tables
create_tables(db)
