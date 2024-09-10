import pytest
from types import SimpleNamespace

def test_add_and_retrieve_contact_success(mock_uow, contact_service):
    """Tests successful creation of a contact record with ContactService"""

    # arrange
    # fixtures
    
    # act
    first_name = 'Janice'
    last_name = 'Doe'
    birthday = '1997-05-21'
    email_address = 'janice.doe@gmails.com'

    contact_service.add(first_name, last_name, birthday, email_address)
    new_contact = contact_service.get_by_id(1)
    new_contact_obj = SimpleNamespace(**new_contact)

    # assert
    assert new_contact is not None
    assert new_contact_obj.first_name == 'Janice'
    assert new_contact_obj.last_name == 'Doe'
    assert new_contact_obj.birthday == '1997-05-21'
    assert new_contact_obj.email_address == 'janice.doe@gmails.com'
    assert mock_uow.committed


def test_add_contact_fail(mock_uow, contact_service):
    """Tests unhappy path when adding a contact record with ContactService - FAIL"""

    # arrange
    first_name = 'Juliet'
    last_name = 'Doe'
    birthday = '1999-07-31'
    email_address = 'juliet.doe@gmails.com'
    contact_service.add(first_name, last_name, birthday, email_address)

    # act
    first_name = 'Juliet'
    last_name = 'Doe'
    birthday = '1999-07-31'
    email_address = 'juliet.doe@gmails.com'
    with pytest.raises(Exception) as excinfo:
        contact_service.add(first_name, last_name, birthday, email_address)
    
    # assert
    assert str(excinfo.value) == 'Contact already exists with this email address - juliet.doe@gmails.com'
    assert mock_uow.committed


def test_get_invalid_contact(contact_service):
    """Tests unhappy path of retrieving a contact that doesn't exist with ContactService"""

    # arrange
    # fixtures

    # assert
    with pytest.raises(Exception) as excinfo:
        contact_service.get_by_id(3)
    
    # assert
    assert str(excinfo.value) == 'No contact found with this id - 3'


def test_get_all_contacts_success(contact_service):
    """Tests happy path of retrieving all contacts with ContactService"""

    # arrange
    first_name = 'Juliet'
    last_name = 'Doe'
    birthday = '1999-07-31'
    email_address = 'juliet.doe@gmails.com'
    contact_service.add(first_name, last_name, birthday, email_address)

    first_name = 'Janice'
    last_name = 'Doe'
    birthday = '1997-05-21'
    email_address = 'janice.doe@gmails.com'
    contact_service.add(first_name, last_name, birthday, email_address)

    # act
    all_contacts = contact_service.get_all_contacts()

    # assert
    assert len(all_contacts) == 2


def test_delete_contact_success(mock_uow, contact_service):
    """Tests happy path of deleting a contact with ContactService"""

    # arrange
    first_name = 'Juliet'
    last_name = 'Doe'
    birthday = '1999-07-31'
    email_address = 'juliet.doe@gmails.com'
    contact_service.add(first_name, last_name, birthday, email_address)

    # act
    contact_service.delete_by_id(1)

    # assert
    assert len(contact_service.get_all_contacts()) == 0
    assert mock_uow.committed


def test_delete_contact_fail(contact_service):
    """Tests unhappy path of deleting a contact that does not exist with ContactService"""

    # arrange
    first_name = 'Juliet'
    last_name = 'Doe'
    birthday = '1999-07-31'
    email_address = 'juliet.doe@gmails.com'

    contact_service.add(first_name, last_name, birthday, email_address)

    # act 
    with pytest.raises(Exception) as excinfo:
        contact_service.delete_by_id(46)
    
    # assert
    assert str(excinfo.value) == 'No contact found with this id - 46'


def test_update_contact_success(mock_uow, contact_service):
    """Tests happy path of updating a contact that exists with ContactService"""

    # arrange
    first_name = 'Juliet'
    last_name = 'Doe'
    birthday = '1999-07-31'
    email_address = 'juliet.doe@gmails.com'
    contact_service.add(first_name, last_name, birthday, email_address)
    current_contact = contact_service.get_by_id(1)

    # act
    new_properties = { 'first_name': 'Jamelia', 'birthday': '1999-07-20'}
    contact_service.update(1, new_properties)
    contact_retrieved = contact_service.get_by_id(1)
    contact_retrieved = SimpleNamespace(**contact_retrieved)
    current_contact = SimpleNamespace(**current_contact)

    # assert
    assert current_contact.email_address == contact_retrieved.email_address
    assert current_contact.last_name == contact_retrieved.last_name
    assert contact_retrieved.first_name == 'Jamelia'
    assert contact_retrieved.birthday == '1999-07-20'
    assert mock_uow.committed == True