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

logging.basicConfig()

blue_dict = dict()
black_dict = dict()
green_dict = dict()
orange_dict = dict()
pink_dict = dict()
red_dict = dict()
yellow_dict = dict()

STATE = {"blue": blue_dict, 'black': black_dict, 'green': green_dict, 'orange': orange_dict, 'pink': pink_dict, 'red': red_dict, 'yellow': yellow_dict}
STATE = {'blue': {'team': 'blue', 'Status': 'Online', 'cur_temp': 16.186622947054673, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'black': {'team': 'black', 'Status': 'Online', 'cur_temp': 18.060239732990127, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'green': {'team': 'green', 'Status': 'Online', 'cur_temp': 19.32267427635639, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'orange': {'team': 'orange', 'Status': 'Online', 'cur_temp': 9.238498490575797, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'pink': {'team': 'pink', 'Status': 'Online', 'cur_temp': 23.115052479850128, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'red': {'team': 'red', 'Status': 'Online', 'cur_temp': 20.562877016701933, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}, 'yellow': {'team': 'yellow', 'Status': 'Online', 'cur_temp': 15.751056340939561, 'min_temp': 10, 'max_temp': 12, 'avg_temp': 14}}
USERS = set()


def state_event():
    return json.dumps(STATE)


def users_event():
    #return json.dumps({"type": "users", "count": len(USERS)})
    return json.dumps(STATE)


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
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
    
    app.listen(8889)
    start_server = websockets.serve(counter, "localhost", 6789)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever() 
 
