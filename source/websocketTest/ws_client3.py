import asyncio
import websockets
from time import sleep

async def test():
 
    async with websockets.connect('ws://localhost:8881/websocket') as websocket:
        
        # 3 messages, 1s delayed 
        for _ in range(3):
            sleep(1)
            await websocket.send("hello from python")
            response = await websocket.recv()
            print(response)

        sleep(1)
 
asyncio.get_event_loop().run_until_complete(test())