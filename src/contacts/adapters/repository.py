from abc import ABC, abstractmethod
import datetime
from types import SimpleNamespace
from sqlalchemy.orm import Session

from src.contacts.domain import model

class AbstractContactRepository(ABC):
    """Common interface for data storage and retrieval operations concerning contacts"""

    @abstractmethod
    def add(self, contact: model.Contact):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, _id: int):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_email_address(self, email_address):
        raise NotImplementedError
    
    @abstractmethod
    def update(self, id, new_properties_dict):
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id):
        raise NotImplementedError


class SqlAlchemyContactRepository(AbstractContactRepository):
    """SQLAlchemy implementation of AbstractContactRepository (for production)"""

    def __init__(self, session: Session):
        self.session = session

    def add(self, contact):
        self.session.add(contact)

    def get_all(self):
        return self.session.query(model.Contact).all()

    def get_by_id(self, id):
        return self.session.query(model.Contact).filter_by(id=id).first()
    
    def get_by_email_address(self, email_address):
        # contacts = self.session.query(model.Contact).filter(model.Contact.email_address == email_address)
        # print(contacts)
        # selected_contacts = contacts.filter_by(email_address=str(email_address)).first()
        return self.session.query(model.Contact).filter_by(email_address=email_address).first()
        # return contacts
    
    def update(self, id, new_properties_dict):
        current_record = self.get_by_id(id)

        for key, value in new_properties_dict.items():
            setattr(current_record, key, value)

    def delete_by_id(self, id):
        selected_contact = self.get_by_id(id)
        self.session.delete(selected_contact)



def find_index(full_list, key, value):
    for i, dictionary in enumerate(full_list):
            if dictionary[key] == value:
                return i
    raise ValueError

class MockContactRepository(AbstractContactRepository):
    """Mock SQLAlchemy implementation of AbstractContactRepository - for (unit) testing"""

    def __init__(self):
        self._data_source = []

    def add(self, contact):
        new_contact = model.Contact.dict(contact)
        new_contact['id'] = len(self._data_source) + 1
        new_contact['created_at'] = datetime.datetime.now()
        self._data_source.append(new_contact)
        return contact
    
    def get_all(self):
        all_contacts = self._data_source
        for contact in all_contacts:
            contact["birthday"] = datetime.date.fromisoformat(contact["birthday"])

        return all_contacts
    
    def get_by_id(self, id):
        selected_contact = [contact for contact in self._data_source if contact.get("id") == id]
        if selected_contact:
            retrieved_contact = selected_contact[0]
            original_contact = selected_contact[0]
            if type(retrieved_contact["birthday"]) != datetime.date:
                retrieved_contact["birthday"] = datetime.datetime.strptime(retrieved_contact["birthday"], "%Y-%m-%d")
            retrieved_contact = model.Contact(**retrieved_contact)
            current_contact_index = find_index(self._data_source, 'id', id)
            original_contact["birthday"] = original_contact["birthday"].strftime("%Y-%m-%d")
            self._data_source[current_contact_index] = original_contact
            return retrieved_contact
        return None            
    
    def get_by_email_address(self, email_address):
        selected_contact = [contact for contact in self._data_source if contact.get("email_address") == email_address]
        if len(selected_contact) > 0:
            retrieved_contact = selected_contact[0]
            original_contact = selected_contact[0]
            retrieved_contact["birthday"] = datetime.datetime.strptime(retrieved_contact["birthday"], "%Y-%m-%d")
            retrieved_contact = model.Contact(**retrieved_contact)
            current_contact_index = find_index(self._data_source, 'email_address', email_address)
            original_contact["birthday"] = original_contact["birthday"].strftime("%Y-%m-%d")
            self._data_source[current_contact_index] = original_contact
            return retrieved_contact
        return None            

    def delete_by_id(self, id):
        for contact in self._data_source:
            if contact['id'] == id:
                self._data_source.remove(contact)
                break

    def update(self, id, new_properties_dict):
        current_record = self.get_by_id(id)
        current_record = vars(current_record)

        for key, value in new_properties_dict.items():
            current_record[key] = value

        current_record.pop('_sa_instance_state', None)

        current_contact_index = find_index(self._data_source, 'id', id)

        self._data_source[current_contact_index] = current_record
        