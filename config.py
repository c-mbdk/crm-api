import os
from click import echo
import pytest
from dotenv import load_dotenv

load_dotenv()

# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False

    if os.getenv('DATABASE_URI'):
        host = os.environ.get('DB_HOST', 'localhost')
        port = 5432 if host == 'localhost' else 54321
        password = os.environ.get('DB_PASSWORD', 'root')
        user, db_name = 'postgres', 'crm_api_db'
        SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, 'instance', 'app.db')}"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ISOLATION_LEVEL = os.getenv('ISOLATION_LEVEL', default='REPEATABLE READ')

class ProductionConfig(Config):
    FLASK_ENV = 'production'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', default=f"sqlite:///{os.path.join(BASEDIR, 'tests', 'test.db')}")
    ISOLATION_LEVEL = 'SERIALIZABLE'

####
#     host = os.environ.get('DB_HOST', 'localhost')
#     port = 5432 if host == 'localhost' else 54321
#     password = os.environ.get('DB_PASSWORD', 'root')
#     user, db_name = 'postgres', 'crm_api_db'
#     return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

def get_api_url():
    # host = os.environ.get('API_HOST', '127.0.0.1')
    # port = 5000
    # return f"http://{host}:{port}"
    return 'http://localhost:5000/'


def register_cli_commands(app):

    @app.cli.command()
    def test():
        """Runs all tests."""
        echo('Running all tests and producing an XML report...')

        exit(pytest.main(["-s", "--junit-xml=test_results/junit.xml", 'tests']))

    @app.cli.command()
    def unittest():
        """Runs all unit tests."""
        pytest.main(["-s", 'tests/unit/'])
        echo('All unit tests have been run.')

    @app.cli.command()
    def integrationtest():
        """Runs all integration tests."""
        pytest.main(["-s", 'tests/integration/'])
        echo('All integration tests have been run.')

    @app.cli.command()
    def endtest():
        """Runs all end-to-end tests."""
        pytest.main(["-s", 'tests/e2e/'])
        echo('All end-to-end tests have been run.')
