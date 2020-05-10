#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import logging
import websockets
import tornado.ioloop
import tornado.web
import tornado.template as template

logging.basicConfig()

STATE = {"value": 0}

USERS = set()


def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


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
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            print(data)
            STATE["value"] = data['temperature']
            await notify_state()
    finally:
        await unregister(websocket)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
    ])
    app.listen(8889)
    start_server = websockets.serve(counter, "localhost", 6789)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever() 
 
