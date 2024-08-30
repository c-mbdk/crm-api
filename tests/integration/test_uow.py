import datetime
import pytest
from sqlalchemy.orm.exc import UnmappedInstanceError

from src.contacts.domain.model import Contact
from src.contacts.service_layer.unit_of_work import SqlAlchemyUnitOfWork

def test_uow_can_add_and_retrieve_contact_success(new_session_empty_db, session_factory):
    """Tests happy path of adding and retrieving a contact with the unit of work"""

    # arrange
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime.strptime('1999-03-13', '%Y-%m-%d'), email_address='julianne.doe@gmails.com')
    uow = SqlAlchemyUnitOfWork(session_factory)

    # act
    with uow:
        uow.contacts.add(contact) 
        retrieved_contact = uow.contacts.get_by_id(1)

    # assert
    assert retrieved_contact.first_name == 'Julianne'
    assert retrieved_contact.email_address == 'julianne.doe@gmails.com'


def test_uow_can_add_and_retrieve_contact_fail(new_session_empty_db, session_factory):
    """Tests unhappy path of adding a contact and retrieving an invalid contact with the unit of work"""

    # arrange
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime.strptime('1999-03-13', '%Y-%m-%d'), email_address='julianne.doe@gmails.com')
    uow = SqlAlchemyUnitOfWork(session_factory)

    # act
    with uow:
        uow.contacts.add(contact)
        retrieved_contact = uow.contacts.get_by_id(45)

    # assert
    assert retrieved_contact is None


def test_uow_can_add_and_retrieve_contact_by_email_address_success(new_session_empty_db, session_factory):
    """Tests happy path of adding and retrieving a contact with the unit of work using the email address"""

    # arrange
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime.strptime('1999-03-13', '%Y-%m-%d'), email_address='julianne.doe@gmails.com')
    uow = SqlAlchemyUnitOfWork(session_factory)

    # act
    with uow:
        uow.contacts.add(contact)
        retrieved_contact = uow.contacts.get_by_email_address('julianne.doe@gmails.com')

    # assert
    assert retrieved_contact.first_name == 'Julianne'
    assert retrieved_contact.last_name == 'Doe'
    assert retrieved_contact.email_address == 'julianne.doe@gmails.com'


def test_uow_can_add_and_retrieve_contact_by_email_address_fail(new_session_empty_db, session_factory):
    """Tests happy path of adding a contact and retrieving an invalid contact with their email address using the unit of work"""

    # arrange
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime.strptime('1999-03-13', '%Y-%m-%d'), email_address='julianne.doe@gmails.com')
    uow = SqlAlchemyUnitOfWork(session_factory)

    # act
    with uow:
        uow.contacts.add(contact)
        retrieved_contact = uow.contacts.get_by_email_address('julianne.d.doe@gmails.com')

    # assert
    assert retrieved_contact is None


def test_uow_can_add_and_retrieve_contacts_success(new_session_empty_db, session_factory):
    """Tests happy path of adding and retrieving multiple contacts with the unit of work"""

    # arrange
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime.strptime('1999-03-13', '%Y-%m-%d'), email_address='julianne.doe@gmails.com')
    second_contact = Contact(first_name='Jacqueline', last_name='Doe', birthday=datetime.datetime.strptime('1992-04-19', '%Y-%m-%d'), email_address='jacqueline.doe@hotmails.com')
    uow = SqlAlchemyUnitOfWork(session_factory)

    # act
    with uow:
        uow.contacts.add(contact)
        uow.contacts.add(second_contact)
        retrieved_contacts = uow.contacts.get_all()

    # assert
    assert len(retrieved_contacts) == 2


def uow_can_delete_contacts_success(new_session_empty_db, session_factory):
    """Tests uow can delete an existing record successfully"""

    # arrange
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime.strptime('1999-03-13', '%Y-%m-%d'), email_address='julianne.doe@gmails.com')
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        uow.contacts.add(contact)
        uow.commit()

    # act
    with uow:
        uow.contacts.delete_by_id(1)
        remaining_contacts = uow.contacts.get_all()
    
    # assert
    assert len(remaining_contacts) is None


def test_uow_does_not_delete_invalid_contacts(new_session_empty_db, session_factory):
    """Tests uow will not delete existing records when an invalid id is provided"""

    # arrange
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime.strptime('1999-03-13', '%Y-%m-%d'), email_address='julianne.doe@gmails.com')
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        uow.contacts.add(contact)
        uow.commit()

    # act
    with uow:
        with pytest.raises(UnmappedInstanceError):
            uow.contacts.delete_by_id(55)
    
    remaining_contacts = uow.contacts.get_all()
    
    # assert
    assert len(remaining_contacts) == 1


def test_uow_rolls_back_uncommitted_work_by_default(new_session_empty_db, session_factory):
    """Tests that uncommitted transactions are rolled back and database remains unchanged"""

    # arrange
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime.strptime('1999-03-13', '%Y-%m-%d'), email_address='julianne.doe@gmails.com')
    second_contact = Contact(first_name='Jacqueline', last_name='Doe', birthday=datetime.datetime.strptime('1992-04-19', '%Y-%m-%d'), email_address='jacqueline.doe@hotmails.com')
    uow = SqlAlchemyUnitOfWork(session_factory)

    # act
    with uow:
        uow.contacts.add(contact)
        uow.contacts.add(second_contact)
    
    retrieved_contacts = uow.contacts.get_all()

    # assert
    assert len(retrieved_contacts) == 0


def test_uow_can_update_contact_successfully(new_session_empty_db, session_factory):
    """Tests happy path where an existing contact can be updated using the unit of work"""

    # arrange
    contact = Contact(first_name='Julianne', last_name='Doe', birthday=datetime.datetime.strptime('1999-03-13', '%Y-%m-%d'), email_address='julianne.doe@gmails.com')
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        uow.contacts.add(contact)
        uow.commit()

    # act
    new_properties = { 'first_name': 'Jamelia', 'birthday': datetime.datetime.strptime('1999-07-20', '%Y-%m-%d')}
    with uow:
        uow.contacts.update(1, new_properties)
        uow.commit()
    
    contact_retrieved = uow.contacts.get_by_id(1)

    # assert
    assert contact_retrieved.first_name == 'Jamelia'
    assert contact_retrieved.last_name == 'Doe'
    assert str(contact_retrieved.birthday) == '1999-07-20'
    assert contact_retrieved.email_address == 'julianne.doe@gmails.com'