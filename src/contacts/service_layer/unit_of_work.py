from __future__ import annotations
import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

import config as config
from src.contacts.adapters.repository import AbstractContactRepository, MockContactRepository, SqlAlchemyContactRepository

# Configuration
def update_config_type(env_type):
    if env_type == "Production":
        config_db_uri = config.ProductionConfig.SQLALCHEMY_DATABASE_URI
        isolation_level = 'REPEATABLE READ'
    else:
        config_db_uri = config.TestingConfig.SQLALCHEMY_DATABASE_URI
        isolation_level = 'SERIALIZABLE'

    return config_db_uri, isolation_level

env_type = os.environ.get('ENV_TYPE')

config_db_uri, isolation_level = update_config_type(env_type)

class AbstractUnitOfWork(abc.ABC):
    contacts: AbstractContactRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self
    
    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config_db_uri,
        isolation_level=isolation_level)
)

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.contacts = SqlAlchemyContactRepository(self.session)
        return super().__enter__()
        
    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class MockUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.contacts = MockContactRepository()
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
