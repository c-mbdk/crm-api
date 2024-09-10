import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from src.contacts.entrypoints.app.application import create_app
from src.contacts.domain import model
from src.contacts.service_layer.services import ContactService

from src.contacts.service_layer.unit_of_work import MockUnitOfWork

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


@pytest.fixture()
def postgres_db():
    engine = create_engine(config.TestingConfig.SQLALCHEMY_DATABASE_URI)
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


@pytest.fixture(scope='module')
def get_flask_app():
    test_flask_app = create_app()

    with test_flask_app.test_client() as testing_client:
        with test_flask_app.app_context():
            yield testing_client