from flask import Flask, request
import psycopg2

# Query: creating contacts table
CREATE_CONTACTS_TABLE = """CREATE TABLE IF NOT EXISTS contacts (id serial PRIMARY KEY,
name varchar(50), age integer, email_address varchar(50), twitter_handle varchar(15), 
CONSTRAINT user_unique UNIQUE (email_address, twitter_handle));
"""


app = Flask(__name__)

connection = psycopg2.connect(database="crm_api_db", user={}, 
                        password={}, host="localhost", port="5432")
     

# VIEW ALL CONTACTS
SELECT_ALL_CONTACTS = """SELECT * FROM contacts;"""

@app.route('/contacts')
def view_all():
    with connection:
        with connection.cursor() as cur:
            cur.execute(CREATE_CONTACTS_TABLE)
            cur.execute(SELECT_ALL_CONTACTS)
            all_contacts = cur.fetchall()    

    return all_contacts


# VIEW ONE CONTACT
SELECT_ONE_CONTACT_TWITTER = """SELECT * FROM contacts WHERE twitter_handle = (%s);"""

@app.get('/contacts/<twitter_handle>')
def view_contact(twitter_handle):
    # data = request.get_json()
    # twitter_handle = data["twitter_handle"]
    with connection:
        with connection.cursor() as cur:
            cur.execute(CREATE_CONTACTS_TABLE)
            cur.execute(SELECT_ONE_CONTACT_TWITTER, (twitter_handle,))
            selected_contact = cur.fetchall()
            if selected_contact:
                return selected_contact
            else:
                return {"message": f"contact with twitter handle {twitter_handle} not found"}, 404


# ADD ONE CONTACT
INSERT_ONE_CONTACT_RETURN_ID = """INSERT INTO contacts (name, age, email_address, twitter_handle) VALUES (%s, %s, %s, %s) RETURNING id;"""

SELECT_ONE_CONTACT_EMAIL_TWITTER = """SELECT * FROM contacts WHERE email_address = (%s) AND twitter_handle = (%s)"""

@app.route('/contacts', methods = ['POST'])
def add_contact():
    data = request.get_json()
    name = data["name"]
    age = data["age"]
    email_address = data["email_address"]
    twitter_handle = data["twitter_handle"]
    if len(twitter_handle) > 15:
        twitter_handle = twitter_handle[0:14]
    with connection:
        with connection.cursor() as cur:
            cur.execute(CREATE_CONTACTS_TABLE)
            cur.execute(SELECT_ONE_CONTACT_EMAIL_TWITTER, (email_address, twitter_handle))
            existing_contact = cur.fetchall()
            if existing_contact:
                return {"message": "Contact already exists with this email address and twitter handle"}, 409
            else: 
                cur.execute(INSERT_ONE_CONTACT_RETURN_ID, (name, age, email_address, twitter_handle,))
                new_contact = cur.fetchone()[0]
                if new_contact:
                    return {"id": new_contact, "message": f"New contact {name} created"}, 201


# UPDATE ONE CONTACT
SELECT_ONE_CONTACT_ID = """SELECT * FROM contacts WHERE id = (%s);"""
UPDATE_CONTACT_BY_ID = """UPDATE contacts SET name = (%s), age = (%s), email_address = (%s), twitter_handle = (%s) WHERE id = (%s)"""

@app.route('/contacts/edit/<int:id>', methods = ['PUT'])
def edit_contact(id):
    with connection:
        with connection.cursor() as cur:
            cur.execute(SELECT_ONE_CONTACT_ID, (id,))
            existing_contact = cur.fetchall()
            if existing_contact:
                updates_for_contact = request.get_json()
                name = updates_for_contact["name"]
                age = updates_for_contact["age"]
                email_address = updates_for_contact["email_address"]
                twitter_handle = updates_for_contact["twitter_handle"]

                cur.execute(UPDATE_CONTACT_BY_ID, (name, age, email_address, twitter_handle, id))
                return {"message": f"Contact with id {id} updated"}
            else:
                return {"message": f"No contact found with id {id}, update failed"}


# DELETE ONE CONTACT
DELETE_ONE_CONTACT_ID = """DELETE FROM contacts WHERE id = (%s)"""

@app.route('/contacts/delete/<int:id>', methods = ['DELETE'])
def delete_contact(id):
    with connection:
            with connection.cursor() as cur:
                cur.execute(SELECT_ONE_CONTACT_ID, (id,))
                existing_contact = cur.fetchall()
                if existing_contact:
                    cur.execute(DELETE_ONE_CONTACT_ID, (id,))
                    return {"message": f"Contact with id {id} deleted"}
                else:
                    return {"message": f"No contact found with id {id}, delete failed"}

if __name__ == "__main__":
    app.run(debug=True)