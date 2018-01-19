import os
import os.path
import sqlite3

# TODO: Add database operations into this file
# TODO: Create database if it does not exist.

DATABASE = 'client_data/clients.db'

def create_database():
    filepath = 'client_data/'
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    filename = os.path.join(filepath, 'clients.db')
    with sqlite3.connect(filename) as conn:
        c = conn.cursor()
        c.execute(
            """CREATE TABLE clients (client_name TEXT, client_website TEXT,
               project TEXT NOT NULL, PRIMARY KEY(client_name))
               """)
    assert os.path.exists(filename)


def destroy_database():
    pass

def create_db_connection(db_name):
    pass
    # connect to the database

def add_client(name, website, project, rate=0):
    # TODO: Add code that allows adding rate to database
    client = (name, website, project)
    # Add this customer to database
    # TODO: Add a try/except clause to catch db not found error
    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO clients VALUES (?,?,?)", client)
            conn.commit()
    except:
        # except OperationalError:
        pass

def delete_client(name):
    pass
    # remove this client from database

def modify_client(name):
    pass

if __name__ == '__main__':
    create_database()