import pytest
import json

from src.contacts.utils.exceptions import BaseCustomException, RecordExists

def test_unhappy_path_create_contact_email_in_use(postgres_test_db_cleardown, get_flask_app):
    """Tests unhappy path of creating a new contact - contact already exists"""

    # arrange
    response_post = get_flask_app.post(
        '/contacts',
        json={'first_name': 'Jane',
              'last_name': 'Doe',
              'birthday': '1997-09-01',
              'email_address': 'jane.doe@gmails.com'}
    )

    # act
    # with pytest.raises(Exception) as excinfo:
    response = get_flask_app.post(
            '/contacts',
            json={'first_name': 'Janice',
                'last_name': 'Doe',
                'birthday': '1999-03-05',
                'email_address': 'jane.doe@gmails.com'}
        )

    # assert
    print(response)
    response_decoded = response.data.decode('utf-8')
    print(response_decoded)
    
    assert "Contact already exists with this email address - jane.doe@gmails.com" in response_decoded


def test_happy_path_retrieve_multiple_contacts(postgres_test_db_cleardown, get_flask_app):
    """Tests happy path - retrieving all contacts via the API, multiple contacts"""

    # arrange
    get_flask_app.post(
        '/contacts',
        json={'first_name': 'June',
              'last_name': 'Doe',
              'birthday': '1997-09-01',
              'email_address': 'june.doe@gmails.com'}
    )

    get_flask_app.post(
        '/contacts',
        json={'first_name': 'Jane',
              'last_name': 'Doe',
              'birthday': '1993-02-10',
              'email_address': 'jone.doe@gmails.com'}
    )

    # act
    response = get_flask_app.get('/contacts')

    response_decoded = response.data.decode('utf-8')
    response_decoded = json.loads(response_decoded)

    # assert
    assert len(response_decoded) == 2


def test_happy_path_contact_creation_update_flow(postgres_test_db_cleardown, get_flask_app):
    """Tests whether the API can handle a complete flow: contact creation, data retrieval, contact updates and contact deletion"""

    # initial creation of contact
    response = get_flask_app.post(
        '/contacts',
        json={'first_name': 'Jane',
              'last_name': 'Doe',
              'birthday': '1997-09-01',
              'email_address': 'jane.doe@gmails.com'}
    )

    resp_decoded = response.data.decode('utf-8')
    resp_decoded = json.loads(resp_decoded)

    # assertions for contact creation
    assert response.status_code == 201
    assert resp_decoded["first_name"] == 'Jane'
    assert resp_decoded["email_address"] == 'jane.doe@gmails.com'

    # separate request to retrieve contact to check persistence - GET
    get_response = get_flask_app.get('/contacts/1')
    get_resp_decoded = get_response.data.decode('utf-8')
    get_resp_decoded = json.loads(get_resp_decoded)

    # assertions for contact retrieval
    assert get_response.status_code == 200
    assert get_resp_decoded["first_name"] == 'Jane'
    assert get_resp_decoded["email_address"] == 'jane.doe@gmails.com'

    # separate request to update contact - PUT
    update_response = get_flask_app.put('/contacts/1', 
                                        json={
                                            'first_name': 'Julianne',
                                            'email_address': 'julianne.doe@gmails.com'})
    
    update_resp_decoded = update_response.data.decode('utf-8')
    update_resp_decoded = json.loads(update_resp_decoded)

    # assertions for contact update
    assert update_response.status_code == 201
    assert update_resp_decoded["first_name"] == 'Julianne'
    assert update_resp_decoded["last_name"] == 'Doe'
    assert update_resp_decoded["birthday"] == '1997-09-01'
    assert update_resp_decoded["email_address"] == 'julianne.doe@gmails.com'


    # separate request for retrieval - check update persisted
    new_get_response = get_flask_app.get('/contacts/1')
    new_get_resp_decoded = new_get_response.data.decode('utf-8')
    new_get_resp_decoded = json.loads(new_get_resp_decoded)

    # assertions for contact retrieval following update
    assert new_get_response.status_code == 200
    assert new_get_resp_decoded["first_name"] == 'Julianne'
    assert new_get_resp_decoded["last_name"] == 'Doe'
    assert new_get_resp_decoded["birthday"] == '1997-09-01'
    assert new_get_resp_decoded["email_address"] == 'julianne.doe@gmails.com'


    # separate request for contact deletion - DELETE
    delete_response = get_flask_app.delete('/contacts/1')

    # assertions for contact deletion
    assert delete_response.status_code == 204
    

    # separate request to confirm contact fully deleted - GET all contacts
    get_all_response = get_flask_app.get('/contacts')
    get_all_resp_decoded = get_all_response.data.decode('utf-8')
    get_all_resp_decoded = json.loads(get_all_resp_decoded)

    # assertions for contact retrieval following delete
    assert get_all_response.status_code == 200
    assert len(get_all_resp_decoded) == 0


    # separate request to confirm contact fully deleted - GET individual contact
    get_single_contact_response = get_flask_app.get('/contacts/1')
    get_single_contact_resp_decoded = get_single_contact_response.data.decode('utf-8')

    # assertions for contact retrieval following delete
    assert 'No contact found with this id - 1' in get_single_contact_resp_decoded


def test_unhappy_path_contact_creation_update_flow(postgres_test_db_cleardown, get_flask_app):
    """Tests whether the API can handle a complete flow: contact creation fails, data retrieval fails, contact updates failure and contact deletion failure"""

    # initial creation of contact
    response = get_flask_app.post(
        '/contacts',
        json={'first_name': 'Jane',
              'last_name': 'Doe',
              'birthday': '1997-09-01',
              'email_address': ''}
    )

    resp_decoded = response.data.decode('utf-8')

    # assertions for contact creation
    assert response.status_code == 422
    assert "Email address must be provided" in resp_decoded


    # separate request to retrieve contact to check record was not committed - GET
    get_response = get_flask_app.get('/contacts/1')
    get_response_decoded = get_response.data.decode('utf-8')

    # assertions for contact retrieval
    assert get_response.status_code == 404
    assert 'No contact found with this id - 1' in get_response_decoded

    # separate request to update contact that was not committed - PUT
    update_response = get_flask_app.put('/contacts/1', json={
        'first_name': 'Julianne','email_address': 'julianne.doe@gmails.com'})
    update_response_decoded = update_response.data.decode('utf-8')

    # assertions for contact update
    assert update_response.status_code == 404
    assert 'No contact found with this id - 1' in update_response_decoded

    # separate request for retrieval - check update did not persist to create a new record
    new_get_response = get_flask_app.get('/contacts/1')
    new_get_response_decoded = new_get_response.data.decode('utf-8')

    # assertions for contact retrieval following attempted update
    assert new_get_response.status_code == 404
    assert 'No contact found with this id - 1' in new_get_response_decoded

    # separate request for attempted contact deletion - DELETE
    delete_response = get_flask_app.delete('/contacts/1')
    delete_response_decoded = delete_response.data.decode('utf-8')
        
    # assertions for attempted contact deletion
    assert delete_response.status_code == 404
    assert 'No contact found with this id - 1' in delete_response_decoded


def test_invalid_path_returns_bad_request(postgres_test_db_cleardown, get_flask_app):
    """Tests invalid path returns Bad Request"""

    # act
    # fixtures

    # arrange
    get_response = get_flask_app.get('/personal_contacts')
    get_response_decoded = get_response.data.decode('utf-8')

    # assert
    assert get_response.status_code == 400
    assert 'Invalid path' in get_response_decoded
    
