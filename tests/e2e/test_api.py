import pytest
import json


def test_unhappy_path_create_contact_email_in_use(postgres_test_db_cleardown, get_flask_app):
    """Tests unhappy path of creating a new contact - contact already exists"""

    # arrange
    get_flask_app.post(
        '/contacts',
        json={'first_name': 'Jane',
              'last_name': 'Doe',
              'birthday': '1997-09-01',
              'email_address': 'jane.doe@gmails.com'}
    )

    # act
    with pytest.raises(Exception) as excinfo:
        response = get_flask_app.post(
            '/contacts',
            json={'first_name': 'Janice',
                'last_name': 'Doe',
                'birthday': '1999-03-05',
                'email_address': 'jane.doe@gmails.com'}
        )

    # assert
    assert str(excinfo.value) == 'Contact already exists with this email address: jane.doe@gmails.com'


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
    with pytest.raises(Exception) as excinfo:
        get_single_contact_response = get_flask_app.get('/contacts/1')

    # assertions for contact retrieval following delete
    assert str(excinfo.value) == 'No contact found with this id: 1'


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
    print(f'Payload validation response: {resp_decoded}')
    # resp_decoded = json.loads(resp_decoded)

    # assertions for contact creation
    assert response.status_code == 422


    # separate request to retrieve contact to check record was not committed - GET
    with pytest.raises(Exception) as excinfo:
        get_response = get_flask_app.get('/contacts/1')
        assert get_response.status_code == 404

    # assertions for contact retrieval
    assert str(excinfo.value) == 'No contact found with this id: 1'

    # separate request to update contact that was not committed - PUT
    with pytest.raises(Exception) as excinfo:
        update_response = get_flask_app.put('/contacts/1', 
                                        json={
                                            'first_name': 'Julianne',
                                            'email_address': 'julianne.doe@gmails.com'})
        assert update_response.status_code == 404


    # assertions for contact update
    assert str(excinfo.value) == 'No contact found with this id: 1'

    # separate request for retrieval - check update did not persist to create a new record
    with pytest.raises(Exception) as excinfo:
        new_get_response = get_flask_app.get('/contacts/1')
        assert new_get_response.status_code == 404

    # assertions for contact retrieval following attempted update
    assert str(excinfo.value) == 'No contact found with this id: 1'

    # separate request for attempted contact deletion - DELETE
    with pytest.raises(Exception) as excinfo:
        delete_response = get_flask_app.delete('/contacts/1')
        assert delete_response.status_code == 404

    # assertions for attempted contact deletion
    assert str(excinfo.value) == 'No contact found with this id: 1'
    
