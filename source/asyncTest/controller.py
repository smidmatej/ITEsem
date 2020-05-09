## Import

import paho.mqtt.client as mqtt
import requests
from json import dumps as dumps_json, loads as loads_json
from datetime import datetime
import re
import sqlite3

import asyncio
import json
import logging
import websockets

## Deklarace

SERVER = '147.228.124.230'  # RPi IP adress
TOPIC = 'ite/#' # Team Blue
DATABASE = 'data.db'

url_base = 'https://uvb1bb4153.execute-api.eu-central-1.amazonaws.com/Prod'
body_login = {'username': 'Blue', 'password': 'n96{ZYV7'}


## Login

def login(body_login):
    url_login = url_base+'/login'
    headers_base_login = {'Content-Type': 'application/json'}
    
    login_data = loads_json(requests.post(url_login, data=dumps_json(body_login), headers=headers_base_login).text)
    
    print('Logged in as ' + login_data['username'])
    print('teamUUID:', login_data['teamUUID'])
    
    return login_data
#teamUUID = 'f32c6941-bc2d-41b2-8bb3-cb6082427613' #blue

## Get sensors

def get_sensors(teamUUID):
    url_sensors = url_base+'/sensors'
    headers_sensors = {'Content-Type': 'application/json', 'teamUUID': teamUUID}
    
    print('Getting sensor for teamUUID: ' + teamUUID)
    sensor_data = loads_json(requests.get(url_sensors, headers=headers_sensors).text)[0]
    
    print('id:' + str(sensor_data['id']) + ', name: ' + sensor_data['name'] + ', sensorUUID: '+ sensor_data['sensorUUID'])
    return sensor_data
#sensorUUIDblue = 'd384a529-6227-4133-afc9-4f5a16665f1f'

## Spojeni s RPi

# Pripojeni k RPi serveru
def on_connect(client, userdata, mid, qos):
    global SERVER
    global TOPIC
    print('Connected to ' + SERVER + r'/' + TOPIC + ' with result code qos:', str(qos))
    
    client.subscribe(TOPIC) #subscribenuti topicu 

async def producer_handler(websocket, path):
    while True:
        message = await on_message()
        await websocket.send(message)

async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        await ws.recv()
        
# Ziskani message ze serveru
def on_message(client, userdata, msg):
    global teamUUID
    global sensorUUID
    
    if (msg.payload == 'Q'):
        client.disconnect()

    print(msg.topic, msg.qos, msg.payload)
    
    mes_dict = message_to_dict(str(msg.payload)) # msg to dict
    
    uri = "ws://localhost:6789"
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(produce(message=json.dumps(mes_dict), host='localhost', port=6789))
    
    if msg.topic == 'ite/blue':
        store_meas(teamUUID, sensorUUID, mes_dict)
    return mes_dict

def store_to_db(mes_dict):
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO measurements VALUES (?,?,?,?)", (mes_dict['source'], mes_dict['team_name'], get_epoch_time_from_date(mes_dict['created_on']), mes_dict['temperature']))
    
    #(source text, team_name text, created_on_timestamp real, temperature real)
    connection.commit()
    connection.close()


## Zpracovani zpravy

def message_to_dict(mes): #prevede MQTT zpravu na dict
    source = re.search("(source){1}", mes).group().strip()
    team_name = re.search("(team_name){1}", mes).group().strip()
    created_on = re.search("(created_on){1}", mes).group().strip()
    temperature = re.search("(temperature){1}", mes).group().strip()
    #print(source + ", " + team_name + ", " + created_on + ", " + temperature)

    source_value = re.search('(?<="source": ").+(?=", "team_name")', mes).group().strip() # "fake"/"real"
    team_name_value = re.search('(?<="team_name": ").+(?=", "created_on")', mes).group().strip() # barva tymu
    created_on_value = re.search('(?<="created_on": ").+(?=", "temperature")', mes).group().strip()
    temperature_value = re.search('(?<="temperature": ).+(?=})', mes).group().strip()
    #print(value1 + ", " + value2 + ", " + value3 + ", " + value4)
    
    mes_dict = {source: source_value, team_name: team_name_value, created_on: created_on_value, temperature: float(temperature_value)}
    
    return mes_dict


def dict_format_for_API(mes_dict): #specialni datetime format pro store measurement v API
    
    time_formated = datetime.strptime(mes_dict['created_on'], '%Y-%m-%dT%H:%M:%S.%f')
    time_formated_appended = time_formated.strftime("%Y-%m-%d") + 'T'+ time_formated.strftime("%H:%M:%S.") + str(int(time_formated.strftime("%f"))//1000) + '+' + '01:00'
    print(mes_dict)
    mes_dict.update({'created_on': time_formated_appended}) # prepise starej format casu na novej
    print(mes_dict)
    return mes_dict

def get_epoch_time_from_date(created_on): #pro created_on
    created_on_formated = datetime.strptime(created_on, '%Y-%m-%dT%H:%M:%S.%f')
    return created_on_formated.timestamp()

## Store measurement
def store_meas(teamUUID, sensorUUID, mes_dict): 
    url_measurement = url_base+'/measurements'
    headers_base_measurement = {'Content-Type': 'application/json', 'teamUUID': teamUUID }
    
    measurement = dict_format_for_API(mes_dict)
    
    print(measurement)
    body_measurement = {'createdOn': measurement['created_on'], 'sensorUUID': sensorUUID, 'temperature': str(round(measurement['temperature'],1)), 'status': 'TEST'}
    
    response = requests.post(url_measurement, data=dumps_json(body_measurement), headers=headers_base_measurement)
    print('Storing measurement to API for teamUUID = ' + teamUUID)
    print(response)
    return response


# Main - pouziti standardu MQTT

if __name__ == '__main__':

    teamUUID = login(body_login)['teamUUID']

    sensor = get_sensors(teamUUID)
    sensorUUID = sensor['sensorUUID']
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set('mqtt_student', password='pivo')

    client.connect(SERVER, 1883, 60)
    '''
    print('ahoj1')
    start_server = websockets.serve(producer_handler, "localhost", 6789)
    print('ahoj')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    '''
    client.loop_forever()
    
    
    
    #mes = str(message.payload)
    #mes = b'{"source": "fake", "team_name": "blue", "created_on": "2020-04-28T20:48:54.850744", "temperature": 22.200536974016668}'
    #mes = str(b'{"source": "fake", "team_name": "blue", "created_on": "2020-04-28T20:48:54.850744", "temperature": 22.200536974016668}')
    
 
