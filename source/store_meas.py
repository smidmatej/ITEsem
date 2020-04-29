## Store measurements

import requests
from json import dumps as dumps_json, loads as loads_json
from datetime import datetime
import ast

# hardcode :)
mes = b'{"source": "fake", "team_name": "blue", "created_on": "2020-04-28T20:48:54.850744", "temperature": 22.200536974016668}'

import ast
mes = str(message.payload)
a = (mes[2:-1])
print(a)
print(type(a))
adict = ast.literal_eval(a)
print(adict)
print(type(adict))
print(adict['source'])


mes = b'{"source": "fake", "team_name": "blue", "created_on": "2020-04-28T20:48:54.850744", "temperature": 22.200536974016668}'
a = (mes[2:-1])
print(a)
print(type(a))
adict = ast.literal_eval(a)
print(adict)
print(type(adict))
print(adict['source'])

teamUUID = 'f32c6941-bc2d-41b2-8bb3-cb6082427613' #blue
sensorUUIDblue = 'd384a529-6227-4133-afc9-4f5a16665f1f'
id = 0
#now = datetime.now()
tms = datetime.strptime(adict['created_on'], '%Y-%m-%dT%H:%M:%S.%f')
time = tms.strftime("%Y-%m-%d") + 'T'+ tms.strftime("%H:%M:%S.") + str(int(tms.strftime("%f"))//1000) + '+' + '01:00'

url_base = 'https://uvb1bb4153.execute-api.eu-central-1.amazonaws.com/Prod'
url_measurement = url_base+'/measurements'
headers_base = {'Content-Type': 'application/json', 'teamUUID': teamUUID }



#body_measurement = {'id': id, 'createdOn': adict['created_on'], 'sensorUUID': sensorUUIDblue, 'temperature': adict['temperature'], 'status': adict['source'], 'modifiedOn': str(now), 'timestamp': now.timestamp()}
body_measurement = {'createdOn': time, 'sensorUUID': sensorUUIDblue, 'temperature': str(round(adict['temperature'],1)), 'status': 'TEST'}

F = requests.post(url_measurement, data=dumps_json(body_measurement), headers=headers_base)
