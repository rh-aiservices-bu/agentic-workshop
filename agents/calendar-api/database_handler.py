import sqlite3


class DatabaseHandler:
    """database handler"""

    def __init__(self, db_name: str, check_same_thread: bool = True):
        """init"""
        self.db_name = db_name
        self.conn = sqlite3.connect(
            '{}.db'.format(db_name), check_same_thread=check_same_thread)
        self.c = self.conn.cursor()

    def execute(self, cmd: str):
        """Execute command"""
        self.c.execute(cmd)
        self.conn.commit()

    def create_table(self, table_name: str, columns: dict):
        """Create table"""
        lst = [str(k) + ' ' + str(v) for k, v in columns.items()]
        columns_str = ','.join(lst)

        cmd = 'CREATE TABLE {table_name}({columns_str})'

        self.execute(cmd.format(
            table_name=table_name,
            columns_str=columns_str))

    def insert_data(self, table_name: str, columns: dict, data: dict):
        """Insert a row of data"""
        lst = ["'" + str(v) + "'" if columns[k] == 'TEXT' else str(v)
               for k, v in data.items()]
        data_str = ','.join(lst)

        cmd = 'INSERT INTO {table_name} VALUES ({data_str})'

        self.execute(cmd.format(
            table_name=table_name,
            data_str=data_str))

    def update_data(self, table_name: str, columns: dict, data: dict, condition: dict):
        """Update data"""
        lst1 = [str(k) + '=' + "'" + str(v) + "'" if columns[k] == 'TEXT'
                else str(k) + '=' + str(v)
                for k, v in data.items()]
        value_str = ','.join(lst1)

        lst2 = [str(k) + '=' + "'" + str(v) + "'" if columns[k] == 'TEXT'
                else str(k) + '=' + str(v)
                for k, v in condition.items()]
        condition_str = ' AND '.join(lst2)

        cmd = 'UPDATE {table_name} SET {value_str} WHERE {condition_str}'

        self.execute(cmd.format(
            table_name=table_name,
            value_str=value_str,
            condition_str=condition_str))

    def delete_data(self, table_name: str, columns: dict, condition: dict):
        """Delete data"""
        lst = [str(k) + '=' + "'" + str(v) + "'" if columns[k] == 'TEXT'
               else str(k) + '=' + str(v)
               for k, v in condition.items()]
        condition_str = ' AND '.join(lst)

        cmd = 'DELETE FROM {table_name} WHERE {condition_str}'

        self.execute(cmd.format(
            table_name=table_name,
            condition_str=condition_str))

    def fetch_data(self, table_name: str, columns: dict, condition: dict):
        """Fetch data"""
        lst = [str(k) + '=' + "'" + str(v) + "'" if columns[k] == 'TEXT'
               else str(k) + '=' + str(v)
               for k, v in condition.items()]
        condition_str = ' AND '.join(lst)

        cmd = 'SELECT * FROM {table_name} WHERE {condition_str}'

        self.execute(cmd.format(
            table_name=table_name,
            condition_str=condition_str))

        return self.c.fetchall()

    def fetch_all(self, table_name: str):
        """Fetch data"""
        cmd = 'SELECT * FROM {table_name}'

        self.execute(cmd.format(
            table_name=table_name))

        return self.c.fetchall()

    def check_existence(self, table_name: str, columns: dict, condition: dict):
        """check the existence of item"""
        try:
            res = self.fetch_data(table_name, columns, condition)
            if len(res) == 0:
                return False
        except Exception:
            return False
        return True


if __name__ == '__main__':
    dbh = DatabaseHandler(db_name="CalendarDB")
    print(dbh.check_existence(
        'calendar',
        {"sid": "TEXT", "name": "TEXT", "content": "TEXT", "category": "TEXT", "level": "INTEGER",
            "status": "REAL", "creation_time": "TEXT", "start_time": "TEXT", "end_time": "TEXT"},
        {"sid": "22"}
    ))
