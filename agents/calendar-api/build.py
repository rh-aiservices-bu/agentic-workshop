import configparser
import json
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

    dbh = database_handler.DatabaseHandler(db_name=db_name)
    dbh.create_table(table_name=table_name, columns=columns)

if __name__ == '__main__':
    build_db()
