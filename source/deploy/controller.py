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
import time
import copy
from statistics import mean
from get_stats import get_stats

## Deklarace

SERVER = '147.228.124.230'  # RPi IP adress
TOPIC = 'ite/#' # Team Blue
DATABASE = 'data.db'

#WS_SERVER = "147.228.121.51" #REMOTE
WS_SERVER = "127.0.0.1" #LOCAL

WS_PORT = 6789

LOW_TEMP = 0
HIGH_TEMP = 30

url_base = 'https://uvb1bb4153.execute-api.eu-central-1.amazonaws.com/Prod'
body_login = {'username': 'Blue', 'password': 'n96{ZYV7'}

alert_state = False
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
    global alert_state
    
    if (msg.payload == 'Q'):
        client.disconnect()
    
    print(msg.topic, msg.qos, msg.payload)
    
    mes_dict = message_to_dict(str(msg.payload)) # msg to dict
    
    if mes_dict != None:
        store_to_db(mes_dict)
        try:
            # send to WS
            stats = get_stats(mes_dict['team_name'])
            mes_to_ws = {'team' : mes_dict['team_name'], 'Status' : 'Online', 'cur_temp' : mes_dict['temperature'] , 'min_temp' : stats[0], 'max_temp' : stats[1], 'avg_temp' : stats[2]}
            loop = asyncio.get_event_loop()
            loop.run_until_complete(produce(message=json.dumps(mes_to_ws), host=WS_SERVER, port=WS_PORT))
        except:
            print('cant connect to server')
            
        if msg.topic == 'ite/blue':
            store_meas(teamUUID, sensorUUID, mes_dict)
        
        #Posilani alertu a checkovani jestli jsme v alertovym stavu
        if not alert_state:
            if check_if_alert(mes_dict) and msg.topic == 'ite/blue':
                #kdyz je teplota alertuhodna a poslal ji blue
                alert_state = True
                store_alert(teamUUID, sensorUUID, mes_dict)
        elif not check_if_alert(mes_dict) and msg.topic == 'ite/blue':
            alert_state = False
        
    
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
    try:
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
    except: 
        print("I'm afraid your journey ends here, traveler ʕᵒ̌n ᵒ̌ʔ ")
        return None
        
    return mes_dict


def dict_format_for_API_meas(mes_dict): #specialni datetime format pro store measurement v API
    
    time_formated = datetime.strptime(mes_dict['created_on'], '%Y-%m-%dT%H:%M:%S.%f')
    time_formated_appended = time_formated.strftime("%Y-%m-%d") + 'T'+ time_formated.strftime("%H:%M:%S.") + str(int(time_formated.strftime("%f"))//1000) + '+' + '01:00'
    
    mes_dict_formated = copy.deepcopy(mes_dict) #deepcopy, jinak se prepise hodnota externe
    mes_dict_formated.update({'created_on': time_formated_appended}) # prepise starej format casu na novej
    print(mes_dict_formated)
    return mes_dict_formated

def get_epoch_time_from_date(created_on): #pro created_on
    created_on_formated = datetime.strptime(created_on, '%Y-%m-%dT%H:%M:%S.%f')
    return created_on_formated.timestamp()

## Store measurement
def store_meas(teamUUID, sensorUUID, mes_dict): 
    url_measurement = url_base+'/measurements'
    headers_base_measurement = {'Content-Type': 'application/json', 'teamUUID': teamUUID }
    
    measurement = dict_format_for_API_meas(mes_dict)
    
    print(measurement)
    body_measurement = {'createdOn': measurement['created_on'], 'sensorUUID': sensorUUID, 'temperature': str(round(measurement['temperature'],1)), 'status': 'TEST'}
    
    response = requests.post(url_measurement, data=dumps_json(body_measurement), headers=headers_base_measurement)
    print('Storing measurement to API for teamUUID = ' + teamUUID)
    print(response)
    return response

def check_if_alert(mes_dict):
    temperature = mes_dict['temperature']

    if (temperature > HIGH_TEMP) or (temperature < LOW_TEMP):
        return True
    return False
    
def store_alert(teamUUID, sensorUUID, mes_dict): 
    #Ulozi do API alert
    url_alert = url_base+'/alerts'
    headers_base_alert = {'Content-Type': 'application/json', 'teamUUID': teamUUID }
    
    alert = dict_format_for_API_alert(mes_dict)
    
    print(alert)
    body_alert = {'createdOn': alert['created_on'], 'sensorUUID': sensorUUID, 'temperature': str(round(alert['temperature'],1)), 'lowTemperature': alert['lowTemperature'], 'highTemperature': alert['highTemperature']}
    
    response = requests.post(url_alert, data=dumps_json(body_alert), headers=headers_base_alert)
    print('Storing alert to API for teamUUID = ' + teamUUID)
    
    return response

def dict_format_for_API_alert(mes_dict):
    time_formated = datetime.strptime(mes_dict['created_on'], '%Y-%m-%dT%H:%M:%S.%f')
    time_formated_appended = time_formated.strftime("%Y-%m-%d") + 'T'+ time_formated.strftime("%H:%M:%S.") + str(int(time_formated.strftime("%f"))//1000) + '+' + '01:00'
    print(mes_dict)
    
    message = {'created_on': time_formated_appended, 'temperature': mes_dict['temperature'], 'lowTemperature': LOW_TEMP, 'highTemperature': HIGH_TEMP}
    return message

def api_online(body_login):

    login_data = login(body_login)  
    
    if login_data['id'] == 4 and login_data['username'] == 'Blue' and login_data['fullName'] == '?, ?, ?, ?' and login_data['year'] == 2020 and login_data['role'] == 'user' and login_data['teamUUID'] == 'f32c6941-bc2d-41b2-8bb3-cb6082427613':
        return 'Online'
    
    else:
        return 'Offline'
'''
## Ziskani statistik
def get_stats(team:str):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    
    today = str(datetime.now().date().day)
    if len(today) == 1:
        today = '0' + today
    
    this_month = str(datetime.now().date().month)
    if len(this_month) == 1:
        this_month = '0' + this_month
    
    # list tuplů (čas, teplota) z databáze
    team_temptime = c.execute('SELECT temperature, created_on_timestamp FROM measurements WHERE team_name = (?)',(team,)).fetchall()
    
    # převedení času na použitelné hodnoty
    team_data = []
    for i in range(0,len(team_temptime)): 
        team_data.append((team_temptime[i][0],time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(team_temptime[i][1]))))    
    
    # zjištění dnešních teplot
    valid_team_data = []
    for i in range(0,len(team_data)):
        if team_data[i][1][5:7] == this_month and team_data[i][1][8:10] == today:
            valid_team_data.append(team_data[i])    
    
    # oddělení dnešních teplot
    team_temp_valid = []
    for i in range(0,len(valid_team_data)):
        team_temp_valid.append(valid_team_data[i][0])
        
    if len(team_temp_valid) == 0:
        return [None,None,None]
    
    ## Provedení statistik
    
    #team min temp
    team_min = min(team_temp_valid)
    print("Dnešní minimální teplota týmu "+team+": "+str(team_min))
    
    #team max temp
    team_max = max(team_temp_valid)
    print("Dnešní maximální teplota týmu " +team+": "+str(team_max))
    
    #team avg temp
    team_avg = mean(team_temp_valid)
    print("Dnešní průměrná teplota týmu " +team+": "+str(team_avg))
    
    return [team_min, team_max, team_avg]
'''
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
    
 
