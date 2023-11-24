import requests
from assertpy import assert_that
from json import dumps

from faker import Faker

BASE_URI = 'http://127.0.0.1:5000/contacts'

# Test Prep: Creating new contacts for test
def create_contact():
    faker = Faker()
    test_contact_name = faker.name()
    test_contact_twitter_handle = '.'.join([faker.first_name(), faker.last_name()])
    test_email = faker.email()

    payload = dumps({
        "name": test_contact_name,
        "age": faker.random_int(18,45),
        "email_address": test_email,
        "twitter_handle": test_contact_twitter_handle
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(BASE_URI, headers=headers, data=payload)
    assert_that(response.status_code).is_equal_to(201)
    return test_contact_name, test_contact_twitter_handle, test_email

# Test Prep: Search response for contact
def search_contact_in(contacts, contact_name):
    all_names = []
    for i in range(len(contacts)):
        all_names.append(contacts[i][1])

    return [name for name in all_names if name == contact_name]

# Test Prep: Get id by contact name
def get_contact_id(contacts, contact_name):

    contact_id= None
    for i in range(len(contacts)):
        if contact_name in contacts[i][1]:
            contact_id = contacts[i][0]
    
    return contact_id


# Test Scenario: Get a list of contacts
def test_get_all_contacts():
    response = requests.get(BASE_URI)
    contacts = response.json()

    assert_that(response.status_code).is_equal_to(200)


# Test Scenario: Get one contact
def test_get_one_contact():
    _, new_test_contact_twitter_handle, _ = create_contact()
    
    url = BASE_URI + f'/{new_test_contact_twitter_handle}'
    
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    assert_that(response.status_code).is_equal_to(200)
    assert_that(len(response.json())).is_equal_to(1)

# Test Scenario: Create a new contact
def test_add_contact():
    new_test_contact_name, _, _ = create_contact()

    all_contacts = requests.get(BASE_URI).json()
    new_created_contact = search_contact_in(all_contacts, new_test_contact_name)
    assert_that(new_created_contact).is_not_empty()

# Test Scenario: Update contact
def test_update_contact():
    new_test_contact_name, _, _ = create_contact()

    all_contacts = requests.get(BASE_URI).json()

    test_contact_id = get_contact_id(all_contacts, new_test_contact_name)

    test_url = BASE_URI + f'/edit/{str(test_contact_id)}'

    faker = Faker()
    updated_name = faker.name()
    updated_age = faker.random_int(18,45)
    updated_email = faker.email()
    updated_twitter_handle = '.'.join([faker.first_name(), faker.last_name()])

    payload = dumps({
        "name": updated_name,
        "age": updated_age,
        "email_address": updated_email,
        "twitter_handle": updated_twitter_handle
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.put(test_url, headers=headers, data=payload)
    assert_that(response.status_code).is_equal_to(200)

    # run this again to refresh contact names
    updated_all_contacts = requests.get(BASE_URI).json()
    updated_contact_name = search_contact_in(updated_all_contacts, updated_name)[0]
    assert_that(updated_contact_name).is_equal_to(updated_name)


# Test Scenario: Delete contact
def test_delete_contact():
    new_test_contact_name, _, _ = create_contact()

    all_contacts = requests.get(BASE_URI).json()

    test_contact_id = get_contact_id(all_contacts, new_test_contact_name)

    test_url = BASE_URI + f'/delete/{str(test_contact_id)}'

    response = requests.delete(test_url)

    assert_that(response.status_code).is_equal_to(200)

# Test Scenario: Unique contacts only
def test_only_unique_contacts():
    new_test_contact_name, new_test_contact_twitter_handle, new_test_email = create_contact()

    faker = Faker()

    payload = dumps({
        "name": new_test_contact_name,
        "age": faker.random_int(),
        "email_address": new_test_email,
        "twitter_handle": new_test_contact_twitter_handle
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(BASE_URI, headers=headers, data=payload)
    assert_that(response.status_code).is_equal_to(409)

