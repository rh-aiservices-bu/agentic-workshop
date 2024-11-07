import configparser
import json
import datetime


class Method:
    """Method"""
    def __init__(self, conf_file):
        """init"""
        self.config = configparser.ConfigParser()
        self.config.read(conf_file)  # 'db.conf'

        self.info = self.config['DEFAULT']
        self.columns = json.loads(self.info['columns'])

    def check_params(self, jsn):
        """检查参数值"""
        if jsn['level'] not in [0, 1, 2, 3]:
            return False

        if jsn['status'] < 0 or jsn['status'] > 1:
            return False

        try:
            lst = [
                jsn['creation_time'],
                jsn['start_time'],
                jsn['end_time']
            ]

            for t in lst:
                _ = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')

        except Exception:
            return False

        return True

    def get(self, dbh, schedule_id):
        return dbh.fetch_data(
            table_name=self.info['table_name'],
            columns=self.columns,
            condition={'sid': schedule_id})

    def post(self, dbh, schedule):
        schedule_id = schedule.dict()['sid']
        if dbh.check_existence(self.info['table_name'], self.columns, {'sid': schedule_id}):
            return False

        if not self.check_params(schedule.dict()):
            return False

        dbh.insert_data(
            table_name=self.info['table_name'],
            columns=self.columns,
            data=schedule.dict())

        return True

    def update(self, dbh, schedule_id, schedule):
        if not dbh.check_existence(self.info['table_name'], self.columns, {'sid': schedule_id}):
            return False

        if not self.check_params(schedule.dict()):
            return False

        dbh.update_data(
            table_name=self.info['table_name'],
            columns=self.columns,
            data=schedule.dict(),
            condition={'sid': schedule_id})

        return True

    def delete(self, dbh, schedule_id):
        if not dbh.check_existence(self.info['table_name'], self.columns, {'sid': schedule_id}):
            return False

        dbh.delete_data(
            table_name=self.info['table_name'],
            columns=self.columns,
            condition={'sid': schedule_id})

        return True


if __name__ == '__main__':
    m = Method(conf_file='db.conf')
