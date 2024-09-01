import os
from flask import Flask
# from flask_migrate import Migrate
from dotenv import load_dotenv
# from flask_marshmallow import Marshmallow
import sqlalchemy as sa

import config
# from src.contacts.adapters.orm import mapper_registry, start_mappers
from src.contacts.entrypoints.routes import init_views
# from db import db
from src.contacts.domain.model import Contact, Base
from src.contacts.domain.schema import ma

# migrate = Migrate()

load_dotenv()

def create_app():

    app = Flask(__name__)
    init_views(app)
    config.register_cli_commands(app)

    config_type_dev = os.environ.get('CONFIG_TYPE')
    print(config_type_dev)
    app.config.from_object(config_type_dev)
    app.config

    # engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    # mapper_registry.metadata.create_all(engine)
    # start_mappers()
    ma.init_app(app)
    # db.init_app(app)
    # migrate.init_app(app,db)

    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("contact"):
        Base.metadata.create_all(engine)
    #     with app.app_context():
    #         db.drop_all()
    #         from src.contacts.domain.model import Contact
    #         db.create_all()

    return app