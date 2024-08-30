# from flask import Flask
# import os
# import sqlalchemy as sa
# from click import echo
# import pytest

# import config
# from src.contacts.adapters.orm import mapper_registry, start_mappers
# from src.contacts.entrypoints.routes import init_views

# def create_app():

#     app = Flask(__name__)
#     init_views(app)
#     register_cli_commands(app)

#     config_type_dev = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
#     app.config.from_object(config_type_dev)

#     engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

#     mapper_registry.metadata.create_all(engine)
#     start_mappers()

#     return app


# def register_cli_commands(app):

#     @app.cli.command()
#     def test():
#         """Runs all tests."""
#         echo('Running all tests and producing an XML report...')

#         exit(pytest.main(["-s", "--minpass=86", "--junit-xml=test_results/junit.xml", 'tests']))

#     @app.cli.command()
#     def unittest():
#         """Runs all unit tests."""
#         pytest.main(["-s", "--cov=src", 'tests/unit/'])
#         echo('All unit tests have been run.')

#     @app.cli.command()
#     def integrationtest():
#         """Runs all integration tests."""
#         pytest.main(["-s", "--cov=src", 'tests/integration/'])
#         echo('All integration tests have been run.')

#     @app.cli.command()
#     def endtest():
#         """Runs all end-to-end tests."""
#         pytest.main(["-s", "--cov=src", 'tests/e2e/'])
#         echo('All end-to-end tests have been run.')

#     # Run tests and generate HTML reports
#     @app.cli.command()
#     def testhtml():
#        """Runs all tests and generates a HTML report."""
#        pytest.main(["-s", "--cov", "--cov-report=html:test_coverage_reports", 'tests'])    
#        echo('All tests have been run and an HTML report has been generated.')