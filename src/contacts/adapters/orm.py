from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime, func
)

from sqlalchemy.orm import registry

from datetime import datetime

from src.contacts.domain import model

metadata = MetaData()

mapper_registry = registry()

contacts = Table(
    'contacts', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String(255)),
    Column('last_name', String(255)),
    Column('birthday', Date, nullable=True),
    Column('email_address', String(255)),
    Column('created', DateTime, default=datetime.utcnow()),
    Column('updated_at', DateTime, onupdate=func.now())
)

def start_mappers():
    mapper_registry.map_imperatively(model.Contact, contacts)