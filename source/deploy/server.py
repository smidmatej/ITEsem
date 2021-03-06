#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import logging
import websockets
import tornado.ioloop
import tornado.web
import tornado.template as template
import os
import sqlite3
from get_history import get_history, get_most_recent_db_entry_for_team

logname = 'logs/server_logs.txt'
logging.basicConfig(filename=logname,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)



STATE = {'blue': {'team': 'blue', 'Status': 'Default', 'cur_temp': 16.18, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'black': {'team': 'black', 'Status': 'Default', 'cur_temp': 18.06, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'green': {'team': 'green', 'Status': 'Default', 'cur_temp': 19.32, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'orange': {'team': 'orange', 'Status': 'Default', 'cur_temp': 9.23, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'pink': {'team': 'pink', 'Status': 'Default', 'cur_temp': 23.11, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'red': {'team': 'red', 'Status': 'Default', 'cur_temp': 20.56, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'yellow': {'team': 'yellow', 'Status': 'Default', 'cur_temp': 15.75, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'API_status' : 'Online'}

HISTORY = {'blue': {'y': [16.18, 12.5], 'x': [1, 2]},
           'black': {'y': [16.18, 12.5], 'x': [1, 2]},
           'green': {'y': [16.18, 12.5], 'x': [1, 2]},
           'orange': {'y': [16.18, 12.5], 'x': [1, 2]},
           'pink': {'y': [16.18, 12.5], 'x': [1, 2]},
           'red': {'y': [16.18, 12.5], 'x': [1, 2]},
           'yellow': {'y': [16.18, 12.5], 'x': [1, 2]}}
USERS = set()

TEAM_NAMES = ('blue', 'black', 'green', 'orange', 'pink', 'red', 'yellow')

#WS_SERVER = "147.228.121.51" #REMOTE
WS_SERVER = "127.0.0.1" #LOCAL
WS_PORT = 6789
HTTP_PORT = 8889

def state_event():
    """Vytvoří zprávu, která je složena ze slovníků STATE a HISTORY pro metodu notify_state"""
    update_history()
    message = {'STATE': STATE, 'HISTORY': HISTORY}
    return json.dumps(message)

def update_history():
    """Pro každý tým aktualizuje slovník HISTORY"""
    for team_name in TEAM_NAMES:
        HISTORY[team_name] = get_history(team_name)

def initialize_state():
    """Pro každý tým inicializuje do slovníku STATE jeho poslední záznam v databázi"""
    for team_name in TEAM_NAMES:
        STATE[team_name] = get_most_recent_db_entry_for_team(team_name)
    
async def notify_state():
    """Každému uživateli zašle zprávu s daty, získanými voláním metody state_event"""
    if USERS:  
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    """Přidá uživatele webového serveru do seznamu uživatelů"""
    USERS.add(websocket)
    logging.info('User logged in')
    await notify_state()


async def unregister(websocket):
    """Odebere uživatele webového serveru do seznamu uživatelů"""
    USERS.remove(websocket)
    logging.info('User logged out')
    await notify_state()


async def counter(websocket, path):
    """Při obdržení zprávy přes websockets aktualizuje API_status ve slovníku STATE a zbylá data uloží pro daný tým do slovníku STATE, následně zavolá metodu notify_state()"""
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            STATE['API_status'] = data['API_status']
            del data['API_status']
            logging.info('Number of users' + str(len(USERS)))
            for team_name in TEAM_NAMES:
                if data['team'] == team_name:
                    STATE[team_name] = data
            await notify_state()
    finally:
        await unregister(websocket)

class MainHandler(tornado.web.RequestHandler):
    """Vykreslí stránku index.html v adresáři web"""
    def get(self):
        self.render('web/index.html')


if __name__ == "__main__":
    
    initialize_state()
    
    handlers = [(r"/", MainHandler),

                ]
    settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "web/static")
            }
    app = tornado.web.Application(handlers, **settings)
    
    app.listen(HTTP_PORT)
    start_server = websockets.serve(counter, WS_SERVER, WS_PORT)
    
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever() 
 
