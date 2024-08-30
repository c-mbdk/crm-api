import datetime
import pytest
from sqlalchemy.orm.exc import UnmappedInstanceError

from src.contacts.adapters.repository import SqlAlchemyContactRepository
from src.contacts.domain.model import Contact


def test_repository_add_and_retrieve_contact_success(new_session_empty_db):
    """Tests happy path when adding a Contact record with the ContactRepository"""

    # arrange
    repo = SqlAlchemyContactRepository(new_session_empty_db)
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.date(1999, 3, 13), email_address='julianne.doe@gmails.com')

    # act
    repo.add(contact)
    new_session_empty_db.commit()
    retrieved_contact = repo.get_by_id(1)

    # assert
    assert retrieved_contact is not None
    assert retrieved_contact.first_name == 'Julianne'
    assert retrieved_contact.last_name == 'Doe'


def test_repository_retrieve_contact_fail(new_session_empty_db):
    """Tests unhappy path when retrieving a Contact record that doesn't exist with the Contact Repository"""

    # arrange
    repo = SqlAlchemyContactRepository(new_session_empty_db)

    # act
    retrieved_contact = repo.get_by_id(444)

    # assert
    assert retrieved_contact is None


def test_repository_add_and_retrieve_multiple_contacts_success(new_session_empty_db):
    """Tests happy path when adding and retrieving multiple contacts with the Contact Repository"""

    # arrange
    repo = SqlAlchemyContactRepository(new_session_empty_db)
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime(1999, 3, 13), email_address='julianne.doe@gmails.com')
    second_contact = Contact(first_name='John', last_name='Doe', birthday=datetime.datetime(1995, 2, 11), email_address='john.doe@gmails.com')

    # act
    repo.add(contact)
    new_session_empty_db.commit()
    repo.add(second_contact)
    new_session_empty_db.commit()
    all_contacts = repo.get_all()

    # assert
    assert len(all_contacts) == 2 


def test_repository_retrieve_contact_by_email_address_success(new_session_empty_db):
    """Tests happy path when retrieving a contact with their email address using the Contact Repository"""

    # arrange
    repo = SqlAlchemyContactRepository(new_session_empty_db)
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime(1999, 3, 13), email_address='julianne.doe@gmails.com')
    repo.add(contact)
    new_session_empty_db.commit()

    # act
    retrieved_contact = repo.get_by_email_address('julianne.doe@gmails.com')

    # assert
    assert retrieved_contact.first_name == 'Julianne'
    assert retrieved_contact.last_name == 'Doe'


def test_repository_retrieve_contact_by_email_address_fail(new_session_empty_db):
    """Tests unhappy path when retrieving a contact with their email address using the Contact Repository - invalid email"""

    # arrange
    repo = SqlAlchemyContactRepository(new_session_empty_db)
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime(1999, 3, 13), email_address='julianne.doe@gmails.com')
    repo.add(contact)
    new_session_empty_db.commit()

    # act
    retrieved_contact = repo.get_by_email_address('julianne.penelope.doe@gmails.com')

    # assert
    assert retrieved_contact is None


def test_repository_update_contact_success(new_session_empty_db):
    """Tests happy path when updating an existing contact using the Contact Repository"""

    # arrange
    repo = SqlAlchemyContactRepository(new_session_empty_db)
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime(1999, 3, 13), email_address='julianne.doe@gmails.com')
    repo.add(contact)
    new_session_empty_db.commit()

    # act
    new_properties = { 'first_name': 'Jamelia', 'birthday': datetime.datetime(1999, 7, 20)}
    repo.update(1, new_properties)
    new_session_empty_db.commit()
    contact_retrieved = repo.get_by_id(1)

    # assert
    assert contact_retrieved.first_name == 'Jamelia'
    assert contact_retrieved.last_name == 'Doe'
    assert contact_retrieved.birthday == datetime.datetime(1999, 7, 20)
    assert contact_retrieved.email_address == 'julianne.doe@gmails.com'


def test_repository_update_contact_fail(new_session_empty_db):
    """Tests unhappy path when updating a contact that doesn't exist with the Contact Repository"""

    # arrange
    repo = SqlAlchemyContactRepository(new_session_empty_db)
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime(1999, 3, 13), email_address='julianne.doe@gmails.com')
    repo.add(contact)
    new_session_empty_db.commit()

    # act
    new_properties = { 'first_name': 'Jamelia', 'birthday': datetime.datetime(1999, 7, 20)}
    with pytest.raises(AttributeError) as excinfo:
        repo.update(366, new_properties)
        new_session_empty_db.commit() 

    # assert
    assert str(excinfo.value) == "'NoneType' object has no attribute 'first_name'"


def test_repository_delete_contact_success(new_session_empty_db):
    """Tests happy path when deleting an existing contact with the Contact Repository"""

    # arrange 
    repo = SqlAlchemyContactRepository(new_session_empty_db)
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime(1999, 3, 13), email_address='julianne.doe@gmails.com')
    repo.add(contact)
    new_session_empty_db.commit()

    # act
    repo.delete_by_id(1)
    new_session_empty_db.commit()
    selected_contact = repo.get_by_id(1)

    # assert
    assert selected_contact is None


def test_repository_delete_contact_fail(new_session_empty_db):
    """Tests unhappy path when deleting a contact with the Contact Repository - the contact does not exist"""

    # arrange 
    repo = SqlAlchemyContactRepository(new_session_empty_db)
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime(1999, 3, 13), email_address='julianne.doe@gmails.com')
    repo.add(contact)
    new_session_empty_db.commit()

    # act
    with pytest.raises(UnmappedInstanceError):
        repo.delete_by_id(63)
        new_session_empty_db.commit()

    all_contacts = repo.get_all()

    # assert
    assert len(all_contacts) == 1