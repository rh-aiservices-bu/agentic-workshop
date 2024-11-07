import requests
import json


class Interface:
    """client interface"""

    def __init__(self, url, app_name):
        self.url = url
        self.app_url = url + '/' + app_name

    def get(self, url, sid):
        """get schedule"""
        url = url + '/' + sid
        return requests.get(url)

    def get_all(self, url, payload=None):
        """get schedules"""
        return requests.get(url, params=payload)

    def post(self, url, data):
        """post schedule"""
        return requests.post(url, data=json.dumps(data))

    def update(self, url, data):
        """update schedule"""
        sid = data['sid']
        url = url + '/' + sid
        return requests.put(url, data=json.dumps(data))

    def delete(self, url, sid):
        """delete schedule"""
        url = url + '/' + sid
        return requests.delete(url)


if __name__ == '__main__':
    url = "http://127.0.0.1:8000"
    i = Interface(url, 'schedules')

    # --------------------------------------
    # get all items
    # --------------------------------------

    # r = i.get_all(i.app_url)

    # --------------------------------------
    # get an item
    # --------------------------------------

    # sid = '1'
    # r = i.get(i.app_url, sid)

    # --------------------------------------
    # post an item
    # --------------------------------------

    data = {
        "sid": "1",
        "name": "John Doe",
        "content": "Test",
        "category": "Business",
        "level": 1,
        "status": 0,
        "creation_time": "2024-11-12 01:23:45",
        "start_time": "2024-11-14 03:20:00",
        "end_time": "2024-11-14 05:30:00"
    }

    r = i.post(i.app_url, data=data)

    # --------------------------------------
    # update an item
    # --------------------------------------

    # data = {
    #     "sid": "1",
    #     "name": "Work",
    #     "content": "Shopping",
    #     "category": "Business",
    #     "level": 1,
    #     "status": 0,
    #     "creation_time": "2024-11-11 01:23:45",
    #     "start_time": "2024-11-12 03:20:00",
    #     "end_time": "2024-11-12 05:30:00"
    # }

    # r = i.update(i.app_url, data=data)

    # --------------------------------------
    # delete an item
    # --------------------------------------

    # sid = "1"
    # r = i.delete(i.app_url, sid)

    # --------------------------------------
    # log
    # --------------------------------------

    print(r)
    print(r.url)
    print(r.ok)
    print(r.content, type(r.content))
    print(r.text, type(r.text))

    # import ast
    # t = ast.literal_eval(r.text)
    # print(t, type(t))
