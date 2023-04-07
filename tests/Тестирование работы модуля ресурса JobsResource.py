import requests
from pprint import pprint

URL_PREFIX = 'http://127.0.0.1:8080/api/v2'

# Проверка работы метода GET
pprint(requests.get(URL_PREFIX + '/jobs').json())
pprint(requests.get(URL_PREFIX + '/jobs/7').json())
pprint(requests.get(URL_PREFIX + '/jobs/0').json())
pprint(requests.get(URL_PREFIX + '/jobs/hfrb').json())

# Проверка работы метода POST
pprint(requests.post(URL_PREFIX + '/jobs',
                        json={
    "id": 100,
    "team_leader": 1,
    "job": "job",
    "work_size": 100,
    "collaborators": [1, 2],
    "start_date": "2024-01-01",
    "end_date": "2024-01-01",
    "is_finished": True,
    "categories": [1, 2, 3]
}).json())
pprint(requests.get(URL_PREFIX + '/jobs').json())
pprint(requests.post(URL_PREFIX + '/jobs',
                        json={
    "id": 100,
    "team_leader": 1,
    "job": "job",
    "work_size": 100,
    "collaborators": [1, 2, 3],
    "start_date": "2024-01-01",
    "end_date": "2024-01-01",
    "is_finished": True,
    "categories": [1, 2, 3]
}).json())
pprint(requests.get(URL_PREFIX + '/jobs/100').json())
pprint(requests.put(URL_PREFIX + '/jobs/100',
                        json={
	"is_finished": True,
	"job": "Сделано в API 2 Updated",
	"categories": [
		1, 3
	]
}).json())
pprint(requests.get(URL_PREFIX + '/jobs/100').json())
pprint(requests.delete(URL_PREFIX + '/jobs/100').json())
pprint(requests.delete(URL_PREFIX + '/jobs/100').json())
pprint(requests.get(URL_PREFIX + '/jobs/100').json())
pprint(requests.get(URL_PREFIX + '/jobs').json())
