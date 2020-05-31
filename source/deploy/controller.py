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
from multiprocessing import Process

## Deklarace

SERVER = '147.228.124.230'  # RPi IP adress
TOPIC = 'ite/#' # Team Blue
DATABASE = 'data.db'
server_status = 'Online'

#WS_SERVER = "147.228.121.51" #REMOTE
WS_SERVER = "127.0.0.1" #LOCAL

WS_PORT = 6789

LOW_TEMP = 0
HIGH_TEMP = 30

url_base = 'https://uvb1bb4153.execute-api.eu-central-1.amazonaws.com/Prod'
body_login = {'username': 'Blue', 'password': 'n96{ZYV7'}

sensor_inc = {'blue' : 0, 'red' : 0, 'green' : 0, 'black': 0, 'yellow' : 0 , 'pink' : 0, 'orange' : 0}
sensor_stat = {'blue' : 'Online', 'red' : 'Online', 'green' : 'Online' , 'black' : 'Online' , 'yellow' : 'Online' , 'pink' : 'Online' , 'orange' : 'Online' }

logname = 'logs/controller_logs.txt'
logging.basicConfig(filename=logname,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

alert_state = False

def login(body_login):
    """Přihlásí uživatele pomocí přihlašovacích údajů v body_login na AIMTEC API"""
    url_login = url_base+'/login'
    headers_base_login = {'Content-Type': 'application/json'}
    
    login_data = loads_json(requests.post(url_login, data=dumps_json(body_login), headers=headers_base_login).text)
    logout = 'Logged in as ' + login_data['username']
    logging.info(logout)
    logout = 'teamUUID:', login_data['teamUUID']
    logging.info(logout)
    
    return login_data

def get_sensors(teamUUID):
    """Požadavek na získání jednotlivých identifikačních kódů senzorů"""
    url_sensors = url_base+'/sensors'
    headers_sensors = {'Content-Type': 'application/json', 'teamUUID': teamUUID}
    
    logout = 'Getting sensor for teamUUID: ' + teamUUID
    logging.info(logout)
    
    sensor_data = loads_json(requests.get(url_sensors, headers=headers_sensors).text)[0]
    logout = 'id:' + str(sensor_data['id']) + ', name: ' + sensor_data['name'] + ', sensorUUID: '+ sensor_data['sensorUUID']
    logging.info(logout)
    
    return sensor_data

def on_connect(client, userdata, mid, qos):
    """Připojení ke komunikačnímu kanálu mqtt"""
    global SERVER
    global TOPIC
    logout = 'Connected to ' + SERVER + r'/' + TOPIC + ' with result code qos:', str(qos)
    logging.info(logout)
    
    client.subscribe(TOPIC)

async def producer_handler(websocket, path):
    while True:
        message = await on_message()
        await websocket.send(message)

async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        await ws.recv()
        
def on_message(client, userdata, msg):
    """Získá data přijaté přes mqtt a odešle je ve formátu json přes protokol websockets

    Metoda získá zprávu přijatou přes mqtt, kterou pomocí metody message_to_dict uloží do slovníku. Pokud je tento slovník prázný, metoda ho vrátí a skončí, pokud prázdný není,
    tak slovník uloží pomocí metody store_to_db do databáze, vypočítá statistiky a vygeneruje zprávu ve formátu json, kterou následně odešle na zadeklarovaný websockets server (proměnná WS_SERVER)
    a port (proměnná WS_PORT). Pokud je zpráva ze senzoru blue, je zavolána metoda store_meas. Metoda ještě zkontroluje, zda pro team blue nedošlo k překročení stanovených hranic. To provede
    zavoláním metody check_if_alert. Pokud je měření neobvyklé, zavolá metodu store_alert, která pošle alert na Aimtec API."""
    global teamUUID
    global sensorUUID
    global alert_state
    global server_status
    global sensor_stat
    global sensor_inc
    
    if (msg.payload == 'Q'):
        client.disconnect()
    logout = str(msg.topic) + str(msg.qos) + str(msg.payload)
    logging.info(logout)
    
    mes_dict = message_to_dict(str(msg.payload))
    
    if mes_dict != None:
        store_to_db(mes_dict)
        if msg.topic == 'ite/blue':
            response = store_meas(teamUUID, sensorUUID, mes_dict)
            if response.status_code >= 500:
                server_status = 'Offline'
            else:
                server_status = 'Online' 
        try:
            sensor_stat[mes_dict['team_name']] = 'Online'
            sensor_inc[mes_dict['team_name']] = 0
            stats = get_stats(mes_dict['team_name'])
            mes_to_ws = {'team' : mes_dict['team_name'], 'Status' : sensor_stat, 'cur_temp' : mes_dict['temperature'] , 'min_temp' : stats[0], 'max_temp' : stats[1], 'avg_temp' : stats[2], 'API_status' : server_status}
            loop = asyncio.get_event_loop()
            loop.run_until_complete(produce(message=json.dumps(mes_to_ws), host=WS_SERVER, port=WS_PORT))
        except:
            logging.info('cant connect to server')
        
        if not alert_state:
            if check_if_alert(mes_dict) and msg.topic == 'ite/blue':
                alert_state = True
                store_alert(teamUUID, sensorUUID, mes_dict)
        elif not check_if_alert(mes_dict) and msg.topic == 'ite/blue':
            alert_state = False
        
    
    return mes_dict

def store_to_db(mes_dict):
    """Uloží přijaté hodnoty ze slovníku mes_dict do databáze"""
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO measurements VALUES (?,?,?,?)", (mes_dict['source'], mes_dict['team_name'], get_epoch_time_from_date(mes_dict['created_on']), mes_dict['temperature']))
    
    connection.commit()
    connection.close()

def message_to_dict(mes): 
    """Pomocí regulárních výrazů převede řetězec mes na slovník. Pokud zpráva neodpovídá danému formátu příjmu dat, vrací None"""
    try:
        source = re.search("(source){1}", mes).group().strip()
        team_name = re.search("(team_name){1}", mes).group().strip()
        created_on = re.search("(created_on){1}", mes).group().strip()
        temperature = re.search("(temperature){1}", mes).group().strip()
        
        source_value = re.search('(?<="source": ").+(?=", "team_name")', mes).group().strip()
        team_name_value = re.search('(?<="team_name": ").+(?=", "created_on")', mes).group().strip()
        created_on_value = re.search('(?<="created_on": ").+(?=", "temperature")', mes).group().strip()
        temperature_value = re.search('(?<="temperature": ).+(?=})', mes).group().strip()
        
        mes_dict = {source: source_value, team_name: team_name_value, created_on: created_on_value, temperature: float(temperature_value)}
    except: 
        logging.info("I'm afraid your journey ends here, traveler ʕᵒ̌n ᵒ̌ʔ ")
        
        return None
        
    return mes_dict


def dict_format_for_API_meas(mes_dict):
    """Převede datetime formát na správný formát pro API - pro measurement"""
    time_formated = datetime.strptime(mes_dict['created_on'], '%Y-%m-%dT%H:%M:%S.%f')
    time_formated_appended = time_formated.strftime("%Y-%m-%d") + 'T'+ time_formated.strftime("%H:%M:%S.") + str(int(time_formated.strftime("%f"))//1000) + '+' + '01:00'
    
    mes_dict_formated = copy.deepcopy(mes_dict) #deepcopy, jinak se prepise hodnota externe
    mes_dict_formated.update({'created_on': time_formated_appended}) # prepise starej format casu na novej
    logging.info(mes_dict_formated)
    
    return mes_dict_formated

def get_epoch_time_from_date(created_on):
    """Z argumentu v datetime formátu získá epoch time"""
    created_on_formated = datetime.strptime(created_on, '%Y-%m-%dT%H:%M:%S.%f')
    return created_on_formated.timestamp()

def store_meas(teamUUID, sensorUUID, mes_dict): 
    """Pomocí HTTP příkazu post zašle mes_dict na Aimtec API jako měření"""
    url_measurement = url_base+'/measurements'
    headers_base_measurement = {'Content-Type': 'application/json', 'teamUUID': teamUUID }
    
    measurement = dict_format_for_API_meas(mes_dict)
    logging.info(measurement)
    
    body_measurement = {'createdOn': measurement['created_on'], 'sensorUUID': sensorUUID, 'temperature': str(round(measurement['temperature'],1)), 'status': 'TEST'}
    
    response = requests.post(url_measurement, data=dumps_json(body_measurement), headers=headers_base_measurement)
    logout = 'Storing measurement to API for teamUUID = ' + teamUUID
    logging.info(logout)
    logging.info(response)
    
    return response

def check_if_alert(mes_dict):
    """Zkontroluje, zda se hodnota v klíči 'temperature' ve slovníku mes_dict vymyká stanoveným hodnotám v proměnných HIGH_TEMP a LOW_TEMP"""
    temperature = mes_dict['temperature']

    if (temperature > HIGH_TEMP) or (temperature < LOW_TEMP):
        return True
    return False
    
def store_alert(teamUUID, sensorUUID, mes_dict): 
    """Pomocí HTTP příkazu post zašle mes_dict na Aimtec API jako Alert"""
    url_alert = url_base+'/alerts'
    headers_base_alert = {'Content-Type': 'application/json', 'teamUUID': teamUUID }
    
    alert = dict_format_for_API_alert(mes_dict)
    
    logging.info(alert)
    
    body_alert = {'createdOn': alert['created_on'], 'sensorUUID': sensorUUID, 'temperature': str(round(alert['temperature'],1)), 'lowTemperature': alert['lowTemperature'], 'highTemperature': alert['highTemperature']}
    
    response = requests.post(url_alert, data=dumps_json(body_alert), headers=headers_base_alert)
    logout = 'Storing alert to API for teamUUID = ' + teamUUID
    logging.info(logout)
    
    return response

def dict_format_for_API_alert(mes_dict):
    """Převede datetime formát na správný formát pro API - pro alert"""
    time_formated = datetime.strptime(mes_dict['created_on'], '%Y-%m-%dT%H:%M:%S.%f')
    time_formated_appended = time_formated.strftime("%Y-%m-%d") + 'T'+ time_formated.strftime("%H:%M:%S.") + str(int(time_formated.strftime("%f"))//1000) + '+' + '01:00'
    
    message = {'created_on': time_formated_appended, 'temperature': mes_dict['temperature'], 'lowTemperature': LOW_TEMP, 'highTemperature': HIGH_TEMP}
    return message

def sensor_status():
    global sensor_inc
    global sensor_stat
    global server_status

    while True:
        sleep(60)
        for key in sensor_inc:
            sensor_inc[key] += 1
        for key in sensor_inc:
            if sensor_inc[key] >= 1:
                sensor_stat[key] = 'Offline'
                stats = get_stats(key)
                mes_to_ws = {'team' : key, 'Status' : sensor_stat[key], 'cur_temp' : 'None', 'min_temp' : stats[0], 'max_temp' : stats[1], 'avg_temp' : stats[2], 'API_status' : server_status}
                loop = asyncio.get_event_loop()
                loop.run_until_complete(produce(message=json.dumps(mes_to_ws), host=WS_SERVER, port=WS_PORT))


if __name__ == '__main__':
    teamUUID = login(body_login)['teamUUID']
    sensor = get_sensors(teamUUID)
    sensorUUID = sensor['sensorUUID']
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.username_pw_set('mqtt_student', password='pivo')
    
    client.connect(SERVER, 1883, 60)

    ###
    p1 = Process(target=sensor_status())
    p1.start()
    p2 = Process(target=client.loop_forever())
    p1.join()
    p2.start()
    p2.join()
    ###

    # client.loop_forever()
    
 
