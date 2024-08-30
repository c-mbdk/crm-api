import pytest
from src.contacts.domain.model import Contact

def test_new_contact_success():
    """Tests happy path of creating a new contact with the domain model"""
    # arrange
    # domain model imported

    # act
    contact = Contact(first_name='Julianne', last_name='Doe', birthday='1999-03-13', email_address='julianne.doe@gmails.com')

    # assert
    assert contact.first_name == 'Julianne'
    assert contact.last_name == 'Doe'
    assert str(contact.birthday) == '1999-03-13'
    assert contact.email_address == 'julianne.doe@gmails.com'


# For the sake of 'code coverage', this one test has been included
# But the assignment + constructor is covered in other tests - the unit tests for the service layer, the integration tests for the repository and unit of work and the end-to-end tests
# So this test could really be removed - there are no special methods in the domain model that warrant testing