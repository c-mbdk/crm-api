from __future__ import annotations
from datetime import date

from marshmallow import ValidationError

from src.contacts.domain import model
from src.contacts.domain import schema
# from src.contacts.adapters.repository import SqlAlchemyContactRepository
from src.contacts.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.contacts.utils.exceptions import RecordExists, InvalidRecord
import config as config

# Configuration
# def update_config_type(env_type):
#     if env_type == 'Production':
#         config_db_uri = config.ProductionConfig.SQLALCHEMY_DATABASE_URI
#     elif env_type == 'Testing':
#         config_db_uri == config.TestingConfig.SQLALCHEMY_DATABASE_URI
#     else:
#         config.db.uri = config.ProductionConfig

#     return config_db_uri

# env_type = 'Production'

# config_db_uri = update_config_type(env_type)

class ContactService:
    # def __init__(self, session):
    #     self.repository = SqlAlchemyContactRepository(session)

    def __init__(self, uow: SqlAlchemyUnitOfWork):
        self.uow = uow

    def add(self, first_name, last_name, birthday, email_address):
        with self.uow:
            contact_exists = self.uow.contacts.get_by_email_address(email_address)
            if contact_exists is not None:
                raise RecordExists(email_address)
            else:
                self.uow.contacts.add(model.Contact(first_name=first_name, last_name=last_name, birthday=birthday, email_address=email_address))
                self.uow.commit()
                retrieved_contact = self.uow.contacts.get_by_email_address(email_address)
                print(f'Raw data from db: {retrieved_contact}')
                print(type(retrieved_contact))
                ready_for_api = serialize_for_api(retrieved_contact, 'single')
                print(f'Data sent to client: {ready_for_api}')
                print(type(ready_for_api))
                return serialize_for_api(retrieved_contact, 'single')
            
    # def add(self, contact):
    #     with self.uow:
    #         contact_exists = self.uow.contacts.get_by_email_address(contact.email_address)
    #         if contact_exists is not None:
    #             raise RecordExists(contact.email_address)
    #         else:
    #             self.uow.contacts.add(contact)
    #             self.uow.commit()
    
    def get_all_contacts(self):
        with self.uow:
            all_contacts = self.uow.contacts.get_all()
            print(f'Retrieved from repo: {all_contacts}')
            return serialize_for_api(all_contacts, 'not single')
    
    def get_by_id(self, id):
        with self.uow:
            contact_exists = self.uow.contacts.get_by_id(id)
            if contact_exists is None:
                raise InvalidRecord(id)
            else:
                selected_contact = self.uow.contacts.get_by_id(id)
                return serialize_for_api(selected_contact, 'single')
            return model.Contact.dict(self.uow.contacts.get_by_id(id))
    
    def get_by_email_address(self, email_address):
        with self.uow:
            contact_exists = self.uow.contacts.get_by_email_address(email_address)
        return model.Contact.dict(contact_exists)
    
    def delete_by_id(self, id):
        with self.uow:
            contact_exists = self.uow.contacts.get_by_id(id)
            if contact_exists is None:
                raise InvalidRecord(id)
            else:
                self.uow.contacts.delete_by_id(id)
                self.uow.commit()
    
    def update(self, id, new_properties_dict):
        with self.uow:
            contact_exists = self.uow.contacts.get_by_id(id)
            if contact_exists is None:
                raise InvalidRecord(id)
                return {'message': 'No contact found with id so update failed.'}
            else:
                with self.uow:
                    if 'birthday' in new_properties_dict.keys():
                        try:
                            new_properties_dict = transform_request_for_db(new_properties_dict)  
                            self.uow.contacts.update(id, new_properties_dict)
                            self.uow.commit()
                            return self.get_by_id(id)
                        except TypeError:
                            return {'message': 'The proposed birthday does not align with requirements.'}
                    else:
                        self.uow.contacts.update(id, new_properties_dict)
                        self.uow.commit()
                        return self.get_by_id(id)
                        # return serialize_for_api(selected_contact, 'single')

                    


# Additional functions for validation - using marshmellow schema

def validate_request_with_schema(request_dict):

    error = None
    validation_schema = schema.ContactSchema()

    try:
        validation_schema.load(request_dict)
    except ValidationError as e:
        error = e

    return error


def transform_request_for_db(request_dict):
    request_dict['birthday'] = date.fromisoformat(request_dict['birthday'])

    return request_dict


def serialize_for_api(contact, list_indicator):
    if str.lower(list_indicator) == 'single':
        serialisation_schema = schema.ContactSchema()
    else:
        serialisation_schema = schema.ContactSchema(many=True)

    try:
        final_output = serialisation_schema.dump(contact)
    except ValidationError as e:
        final_output = ValidationError
    return final_output

