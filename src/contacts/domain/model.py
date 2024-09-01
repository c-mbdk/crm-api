from __future__ import annotations

from sqlalchemy import func
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    email_address = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    last_updated_at = Column(DateTime, nullable=False, default=datetime.now(),onupdate=func.now())

    def __repr__(self):
        return f'id: {self.id}, \
                first_name: {self.first_name}, \
                last_name: {self.last_name}, \
                birthday: {self.birthday}, \
                email_addres: {self.email_address}, \
                created_at: {self.created_at}'

    def dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthday": self.birthday,
            "email_address": self.email_address,
            "created_at": self.created_at
        }