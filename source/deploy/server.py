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
from get_history import get_history

logging.basicConfig()

STATE = {'blue': {'team': 'blue', 'Status': 'Default', 'cur_temp': 16.18, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'black': {'team': 'black', 'Status': 'Default', 'cur_temp': 18.06, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'green': {'team': 'green', 'Status': 'Default', 'cur_temp': 19.32, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'orange': {'team': 'orange', 'Status': 'Default', 'cur_temp': 9.23, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'pink': {'team': 'pink', 'Status': 'Default', 'cur_temp': 23.11, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'red': {'team': 'red', 'Status': 'Default', 'cur_temp': 20.56, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'yellow': {'team': 'yellow', 'Status': 'Default', 'cur_temp': 15.75, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}}

HISTORY = {'blue': {'y': [16.18, 12.5], 'x': [1, 2]},
           'black': {'y': [16.18, 12.5], 'x': [1, 2]},
           'green': {'y': [16.18, 12.5], 'x': [1, 2]},
           'orange': {'y': [16.18, 12.5], 'x': [1, 2]},
           'pink': {'y': [16.18, 12.5], 'x': [1, 2]},
           'red': {'y': [16.18, 12.5], 'x': [1, 2]},
           'yellow': {'y': [16.18, 12.5], 'x': [1, 2]}}
USERS = set()

#WS_SERVER = "147.228.121.51" #REMOTE
WS_SERVER = "127.0.0.1" #LOCAL
WS_PORT = 6789
HTTP_PORT = 8889

def state_event():
    message = {'STATE': STATE}
    return json.dumps(message)


def new_user_login():
    #return json.dumps({"type": "users", "count": len(USERS)})
    update_history() #aktualizuje promenou HISTORY z databaze
    message = {'STATE': STATE, 'HISTORY': HISTORY} # pri pripojeni noveho klienta posle momentalni stav a data z minulosti
    print(HISTORY)
    return json.dumps(message)

def update_history():
    history_blue = get_history('blue')
    history_black = get_history('black')
    history_green = get_history('green')
    history_orange = get_history('orange')
    history_pink = get_history('pink')
    history_red = get_history('red')
    history_yellow = get_history('yellow')
    
    HISTORY['blue'] = history_blue
    HISTORY['black'] = history_black
    HISTORY['green'] = history_green
    HISTORY['orange'] = history_orange
    HISTORY['pink'] = history_pink
    HISTORY['red'] = history_red
    HISTORY['yellow'] = history_yellow
    
async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = new_user_login()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    print('User logged in')
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    print('User logged out')
    await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            print(data)
            print('Number of users' + str(len(USERS)))
            if data['team'] == 'blue':
                STATE['blue'] = data
            
            elif data['team'] == 'black':
                STATE['black'] = data
                
            elif data['team'] == 'green':
                STATE['green'] = data
                
            elif data['team'] == 'orange':
                STATE['orange'] = data
                
            elif data['team'] == 'pink':
                STATE['pink'] = data
                
            elif data['team'] == 'red':
                STATE['red'] = data
                
            elif data['team'] == 'yellow':
                STATE['yellow'] = data
            else:
                print('server dostal dato krery neodpovida formatu')
            print('STATE' + str(STATE))
            await notify_state()
    finally:
        await unregister(websocket)
#STATE = {"blue": blue_dict, 'black': black_dict, 'green': green_dict, 'orange': orange_dict, 'pink': pink_dict, 'red': red_dict, 'yellow': yellow_dict}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('web/index.html')


if __name__ == "__main__":
    handlers = [(r"/", MainHandler),

                ]
    settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "web/static")
            }
    print(settings["static_path"])
    print(os.path.dirname(__file__))
    print(__file__)
    app = tornado.web.Application(handlers, **settings)
    
    app.listen(HTTP_PORT)
    start_server = websockets.serve(counter, WS_SERVER, WS_PORT)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever() 
 
