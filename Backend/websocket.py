import asyncio
import websockets

port = 8765

async def hello(websocket):
    while True:

        message = await websocket.recv()
        print(f"<<< {message}")

        #await websocket.send()

async def main():
    async with websockets.serve(hello, "localhost", port):
        print(f"Websocket server started on:  localhost:{port}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())