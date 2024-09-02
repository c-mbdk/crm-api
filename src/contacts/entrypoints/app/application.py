import os
from flask import Flask
from dotenv import load_dotenv
import sqlalchemy as sa

import config
from src.contacts.entrypoints.routes import init_views
from src.contacts.domain.model import Base
from src.contacts.domain.schema import ma

load_dotenv()

def create_app():

    app = Flask(__name__)
    init_views(app)
    config.register_cli_commands(app)

    config_type_dev = os.environ.get('CONFIG_TYPE')
    print(config_type_dev)
    app.config.from_object(config_type_dev)
    app.config

    ma.init_app(app)

    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("contact"):
        Base.metadata.create_all(engine)

    return app