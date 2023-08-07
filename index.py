from flask import Flask
import psycopg2
import pandas as pd

app = Flask(__name__)

conn = psycopg2.connect(database="crm_api_db", user="postgres", 
                        password="root", host="localhost", port="5432")

cur = conn.cursor()

# Creating tables if they don't already exist
cur.execute("""CREATE TABLE IF NOT EXISTS contacts (id serial PRIMARY KEY,
name varchar(50), age integer, email_address varchar(50), twitter_handle varchar(15), 
CONSTRAINT user_unique UNIQUE (email_address , twitter_handle))
""")
     
# inserting basic data
cur.execute("""INSERT INTO contacts (name, age, email_address, twitter_handle) 
VALUES ('Jane Doe', 20, 'jane.doe@gmails.com', '@janedoe_twt')""")
            
conn.commit()
cur.close()
conn.close()

@app.route('/contacts')
def view_all():
    conn = psycopg2.connect(database="crm_api_db",
                            user="postgres",
                            password="root",
                            host="localhost", port="5432")
    
    cur = conn.cursor()

    cur.execute("""SELECT * FROM contacts""")

    data = cur.fetchall()

    return pd.to_json(data)

@app.route('/contacts', methods = ['POST'])
def add_contact():
    pass

# @app.route('', methods = [])
# def edit_contact():
#     pass

# @app.route('', methods = ['DELETE'])
# def delete_contact():
#     pass

if __name__ == "__main__":
    app.run()