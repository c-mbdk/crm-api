from __future__ import annotations

from sqlalchemy import func
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, String, Date
from sqlalchemy.orm import declarative_base

from src.contacts.utils.custom_types import Name, CustomDate, EmailValidator, EmailAddress
from src.contacts.utils.serializers import serialise_datetime

# from db import db

Base = declarative_base()
# metadata = Base.metadata


# class Contact(db.Model):
#     __tablename__ = "contact"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     first_name = db.Column(db.String(255), nullable=False)
#     last_name = db.Column(db.String(255), nullable=False)
#     birthday = db.Column(db.DateTime(timezone=True), nullable=True)
#     email_address = db.Column(db.String(255),nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, default = datetime.now(timezone.utc))
#     last_updated_at = db.Column(db.DateTime, nullable=False, onupdate=func.now())

#     # def __init__(self, first_name, last_name, birthday, email_address):
#     #     self.first_name = first_name
#     #     self.last_name = last_name
#     #     self.birthday = birthday
#     #     self.email_address = email_address
#     #     self.created_at = datetime.now(timezone.utc)

#     def __repr__(self):
#         return f'id: {self.id}, \
#                 first_name: {self.first_name}, \
#                 last_name: {self.last_name}, \
#                 birthday: {self.birthday}, \
#                 email_addres: {self.email_address}, \
#                 created_at: {self.created_at}'

#     def dict(self):
#         return {
#             "id": self.id,
#             "first_name": self.first_name,
#             "last_name": self.last_name,
#             "birthday": self.birthday,
#             "email_address": self.email_address,
#             "created_at": self.created_at
#         }


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
    



# class Contact:

#     first_name = Name()
#     last_name = Name()
#     birthday = CustomDate()
#     email_address = EmailAddress()


#     def __init__(self, first_name, last_name, birthday, email_address):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.birthday = birthday
#         self.email_address = email_address

#     def __repr__(self):
#         return f"'<Person: {self.first_name} {self.last_name}>'"
    
#     def get_contact_dict(self):
#         return {
#             'first_name': self.first_name,
#             'last_name': self.last_name,
#             'birthday': serialise_datetime(self.birthday),
#             'email_address': self.email_address
#         }