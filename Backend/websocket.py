import asyncio
import websockets
from Classes import game

port = 8765

async def hello(websocket):
    while True:

        message = await websocket.recv()
        print(f"<<< {message}")

        response = "python socket received message"
        await websocket.send(response)
        print(f"<<< {response}")

async def startWSS():
    async with websockets.serve(hello, "localhost", port):
        print(f"Websocket server started on:  localhost:{port}")
        await asyncio.Future()  # run forever

asyncio.run(startWSS())