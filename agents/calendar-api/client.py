import requests
import json

class Interface:
    def __init__(self, base_url, app_name):
        self.app_url = f"{base_url}/{app_name}"

    def _make_request(self, method, endpoint="", **kwargs):
        url = f"{self.app_url}/{endpoint}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()  # Raise an error for unsuccessful status codes
        return response.json()

    def get(self, sid):
        return self._make_request("GET", endpoint=sid)

    def get_all(self, payload=None):
        return self._make_request("GET", params=payload)

    def post(self, data):
        headers = {'Content-Type': 'application/json'}
        return self._make_request("POST", headers=headers, data=json.dumps(data))

    def update(self, sid, data):
        headers = {'Content-Type': 'application/json'}
        return self._make_request("PUT", endpoint=sid, headers=headers, data=json.dumps(data))

    def delete(self, sid):
        return self._make_request("DELETE", endpoint=sid)

if __name__ == '__main__':
    url = "http://127.0.0.1:8000"
    i = Interface(url, 'schedules')

    data = {
        "sid": "2",
        "name": "John Doe",
        "content": "Test",
        "category": "Business",
        "level": 1,
        "status": 0,
        "creation_time": "2024-11-12 01:23:45",
        "start_time": "2024-11-14 03:20:00",
        "end_time": "2024-11-14 05:30:00"
    }

    r = i.post(data=data)
    print(r)
