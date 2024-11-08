import sqlite3

class DatabaseHandler:
    def __init__(self, db_name: str, check_same_thread: bool = True):
        self.db_name = db_name
        self.conn = sqlite3.connect(f'{db_name}.db', check_same_thread=check_same_thread)
        self.c = self.conn.cursor()

    def execute(self, cmd: str, params=()):
        try:
            self.c.execute(cmd, params)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def create_table(self, table_name: str, columns: dict):
        columns_str = ', '.join([f"{k} {v}" for k, v in columns.items()])
        cmd = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})'
        self.execute(cmd)

    def insert_data(self, table_name: str, columns: dict, data: dict):
        placeholders = ', '.join('?' for _ in data)
        cmd = f'INSERT INTO {table_name} ({", ".join(data.keys())}) VALUES ({placeholders})'
        self.execute(cmd, tuple(data.values()))

    def update_data(self, table_name: str, data: dict, condition: dict):
        data_str = ', '.join([f"{k} = ?" for k in data.keys()])
        cond_str = ' AND '.join([f"{k} = ?" for k in condition.keys()])
        cmd = f'UPDATE {table_name} SET {data_str} WHERE {cond_str}'
        self.execute(cmd, tuple(data.values()) + tuple(condition.values()))

    def delete_data(self, table_name: str, condition: dict):
        cond_str = ' AND '.join([f"{k} = ?" for k in condition.keys()])
        cmd = f'DELETE FROM {table_name} WHERE {cond_str}'
        self.execute(cmd, tuple(condition.values()))

    def fetch_data(self, table_name: str, condition: dict = None):
        if condition:
            cond_str = ' AND '.join([f"{k} = ?" for k in condition.keys()])
            cmd = f'SELECT * FROM {table_name} WHERE {cond_str}'
            self.execute(cmd, tuple(condition.values()))
        else:
            cmd = f'SELECT * FROM {table_name}'
            self.execute(cmd)
        return self.c.fetchall()

    def check_existence(self, table_name: str, condition: dict):
        result = self.fetch_data(table_name, condition)
        return bool(result)

if __name__ == '__main__':
    dbh = DatabaseHandler(db_name="CalendarDB")
    print(dbh.check_existence(
        'calendar',
        {"sid": "TEXT", "name": "TEXT", "content": "TEXT", "category": "TEXT", "level": "INTEGER",
         "status": "REAL", "creation_time": "TEXT", "start_time": "TEXT", "end_time": "TEXT"},
        {"sid": "22"}
    ))
