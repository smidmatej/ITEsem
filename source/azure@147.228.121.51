#login

import requests
from json import dumps as dumps_json, loads as loads_json

url_base = 'https://uvb1bb4153.execute-api.eu-central-1.amazonaws.com/Prod'
headers_base = {'Content-Type': 'application/json'}

# login
url_login = url_base+'/login'
body_login = {'username': 'Blue', 'password': 'n96{ZYV7'}

login_data = loads_json(requests.post(url_login, data=dumps_json(body_login), headers=headers_base).text)
print('\nLogin data:', login_data)

teamUUID = login_data['teamUUID']
print('\nteamUUID:', teamUUID)

# get sensors
url_sensors = url_base+'/sensors'
headers_sensors = dict(headers_base)
headers_sensors.update({'teamUUID': teamUUID})

sensors_data = requests.get(url_sensors, headers=headers_sensors)
print('\nSensors data:', loads_json(sensors_data.text))