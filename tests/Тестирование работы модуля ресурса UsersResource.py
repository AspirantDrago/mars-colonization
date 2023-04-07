import requests
from pprint import pprint


URL_PREFIX = 'http://127.0.0.1:8080/api/v2'
pprint(requests.get(URL_PREFIX + '/users').json())
pprint(requests.get(URL_PREFIX + '/users/7').json())
pprint(requests.get(URL_PREFIX + '/users/0').json())
pprint(requests.get(URL_PREFIX + '/users/wv').json())

pprint(requests.post(URL_PREFIX + '/users',
                     json={
	"id": 100,
	"address": "Ниоткуда",
	"age": 100,
	"email": "mail@mail.ru",
	"name": "name",
	"position": "position",
	"speciality": "speciality"
}).json())
pprint(requests.post(URL_PREFIX + '/users',
                     json={
	"id": 100,
	"address": "Ниоткуда",
	"age": 100,
	"email": "mail@mail.ru",
	"name": "name",
	"position": "position",
	"speciality": "speciality"
}).json())
pprint(requests.get(URL_PREFIX + '/users/100').json())

pprint(requests.put(URL_PREFIX + '/users/100',
                     json={
	"address": "Нигде",
	"age": 101,
	"email": "pochta@mail.ru",
	"surname": "surname"
}).json())
pprint(requests.get(URL_PREFIX + '/users/100').json())

pprint(requests.delete(URL_PREFIX + '/users/100').json())
pprint(requests.delete(URL_PREFIX + '/users/100').json())
pprint(requests.get(URL_PREFIX + '/users/100').json())

pprint(requests.get(URL_PREFIX + '/users').json())
