import os
import configparser
import json
import sqlite3
import database_handler

def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['DEFAULT']

def build_db():
    info = load_config('db.conf')
    db_name = info.get('db_name')
    table_name = info.get('table_name')
    columns = json.loads(info.get('columns', '{}'))

    if not db_name or not table_name or not columns:
        raise ValueError("Database configuration is incomplete.")

    db_path = f"{db_name}.db"

    # Check if the database file already exists
    if os.path.exists(db_path):
        print(f"Database file '{db_path}' already exists.")
        dbh = database_handler.DatabaseHandler(db_name=db_name)
        
        # Check if the table exists
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            table_exists = cursor.fetchone()[0] == 1
            connection.close()

            if table_exists:
                print(f"Table '{table_name}' already exists. No action needed.")
                return
            else:
                print(f"Table '{table_name}' does not exist. Creating table...")
                dbh.create_table(table_name=table_name, columns=columns)

        except Exception as e:
            print(f"An error occurred while checking the table existence: {e}")
            raise

    else:
        print(f"Database file '{db_path}' does not exist. Creating database and table...")
        dbh = database_handler.DatabaseHandler(db_name=db_name)
        dbh.create_table(table_name=table_name, columns=columns)

if __name__ == '__main__':
    build_db()
