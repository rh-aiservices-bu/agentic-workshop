import configparser
import json
import database_handler


def build_bd():
    config = configparser.ConfigParser()
    config.read('db.conf')
    info = config['DEFAULT']

    dbh = database_handler.DatabaseHandler(db_name=info['db_name'])

    dbh.create_table(
        table_name=info['table_name'],
        columns=json.loads(info['columns']))


if __name__ == '__main__':
    build_bd()
