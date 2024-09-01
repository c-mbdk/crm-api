import time
from pathlib import Path
import os

import pytest
import requests

from unittest.mock import create_autospec
from requests.exceptions import ConnectionError
import sqlalchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers, Session

import config
from src.contacts.adapters.orm import mapper_registry, start_mappers
from src.contacts.entrypoints.app.application import create_app
from src.contacts.domain import model
from src.contacts.service_layer.services import ContactService
# import db

from src.contacts.service_layer.unit_of_work import MockUnitOfWork


os.environ["ENV_TYPE"] = "Testing"
os.environ["CONFIG_TYPE"] = "config.TestingConfig"
os.environ["ISOLATION_LEVEL"] = "SERIALIZABLE"


@pytest.fixture
def mock_uow():
    unit_of_work = MockUnitOfWork()
    return unit_of_work

@pytest.fixture
def contact_service(mock_uow):
    contact_service = ContactService(mock_uow)
    return contact_service

@pytest.fixture
def in_memory_db():
    engine = create_engine('sqlite:///:memory:')
    model.Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def session_factory(in_memory_db):
    yield sessionmaker(bind=in_memory_db)

@pytest.fixture
def session(session_factory):
    return session_factory(expire_on_commit=False)

@pytest.fixture
def new_session_empty_db(session):
    results = session.query(model.Contact).all()
    for contact in results:
        session.delete(contact)
        session.commit()
    
    results_post_delete = session.query(model.Contact).all()
    if results_post_delete == []:
        return session
    raise Exception('All contacts were not deleted')


def wait_for_postgres_to_start_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail('Postgres never started up')

def wait_for_webapp_to_start_up():
    deadline = time.time() + 10
    url = config.get_api_url()
    while time.time() < deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            time.sleep(0.5)
    pytest.fail('API never started up')


@pytest.fixture()
def postgres_db():
    engine = create_engine(config.TestingConfig.SQLALCHEMY_DATABASE_URI)
    # wait_for_postgres_to_start_up(engine)
    model.Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def postgres_db_session_factory(postgres_db):
    yield sessionmaker(bind=postgres_db)

@pytest.fixture
def postgres_db_session(postgres_db_session_factory):
    return postgres_db_session_factory()

@pytest.fixture
def postgres_test_db_cleardown(postgres_db):
    model.Base.metadata.drop_all(postgres_db)
    model.Base.metadata.create_all(postgres_db)

    # results = postgres_db_session.query(model.Contact).all()
    # for contact in results:
    #     postgres_db_session.delete(contact)
    #     postgres_db_session.commit()
    
    # results_post_delete = postgres_db_session.query(model.Contact).all()
    # print(results_post_delete)
    # if results_post_delete == []:
    #     postgres_db_session.close()
    # else:
    #     pytest.fail('All contacts were not deleted')

# @pytest.fixture
# def postgres_session(postgres_session_factory):
#     return postgres_session_factory()


@pytest.fixture(scope='module')
def get_flask_app():
    # os.environ['CONFIG_TYPE'] = "config.TestingConfig"
    os.environ["ENV_TYPE"] = "Testing"
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    os.environ["ISOLATION_LEVEL"] = "SERIALIZABLE"
    test_flask_app = create_app()

    with test_flask_app.test_client() as testing_client:
        with test_flask_app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def test_flask_client(get_flask_app):
    return get_flask_app.test_client()

@pytest.fixture
def restart_api():
    (Path(__file__).parent / '../src/contacts/entrypoints/flask_app.py').touch()
    time.sleep(0.5)
    wait_for_webapp_to_start_up()

@pytest.fixture
def mock_session() -> Session:
    session = create_autospec(Session)
    return session
