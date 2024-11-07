import configparser
import json
import datetime

class Method:
    def __init__(self, conf_file):
        self.config = configparser.ConfigParser()
        self.config.read(conf_file)
        self.info = self.config['DEFAULT']
        self.columns = json.loads(self.info['columns'])

    def check_params(self, jsn):
        if jsn['level'] not in [0, 1, 2, 3]:
            return False
        if not (0 <= jsn['status'] <= 1):
            return False
        try:
            for t in ['creation_time', 'start_time', 'end_time']:
                datetime.datetime.strptime(jsn[t], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return False
        return True

    def get(self, dbh, schedule_id):
        return dbh.fetch_data(
            table_name=self.info['table_name'],
            condition={'sid': schedule_id})

    def post(self, dbh, schedule):
        if dbh.check_existence(self.info['table_name'], {'sid': schedule.sid}):
            return False
        if not self.check_params(schedule.dict()):
            return False
        dbh.insert_data(self.info['table_name'], self.columns, schedule.dict())
        return True

    def update(self, dbh, schedule_id, schedule):
        if not dbh.check_existence(self.info['table_name'], {'sid': schedule_id}):
            return False
        if not self.check_params(schedule.dict()):
            return False
        dbh.update_data(self.info['table_name'], schedule.dict(), {'sid': schedule_id})
        return True

    def delete(self, dbh, schedule_id):
        if not dbh.check_existence(self.info['table_name'], {'sid': schedule_id}):
            return False
        dbh.delete_data(self.info['table_name'], {'sid': schedule_id})
        return True

if __name__ == '__main__':
    m = Method(conf_file='db.conf')
