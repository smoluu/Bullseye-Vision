import asyncio
import websockets as ws
from Classes import game
import json
import base64

port = 8765
clients = []

async def sendData(ws,data):
        data = json.dumps(data)
        await ws.send(data)
        print(f"SENT: {data}")

# sends images of dartboar if there is clients
async def sendImage(ws):
        while True:
                if len(clients) > 0:
                    # insert dartboard image here
                    with open("Backend/testimg.png", "rb") as image:
                         image = image.read()
                    image = base64.b64encode(image).decode("utf-8")
                    data = {
                         "type": "image",
                         "content": image
                    }
                    
                    await ws.send(json.dumps(data))
                    await asyncio.sleep(1)
                else:
                    await asyncio.sleep(1)

async def handleConnection(ws):

    await ws.send("Connection succesfull")

    async def receiveData(ws):
          while True:
                try:
                    data = await ws.recv()
                    data = json.loads(data)

                    if "clients" in data:
                        global clients
                        clients = data["clients"]
                        print(f"Clients: {clients}")
                        len(clients)
                    if "message" in data:
                        print(f"Message received: {data["message"]}")


                except ws.exceptions.ConnectionClosed as e:
                    # Handle connection closed exception
                    print(f"Connection closed: {e}")

                except ws.exceptions.WebSocketException as e:
                    # Handle other WebSocket exceptions
                    print(f"WebSocket exception: {e}")

                except Exception as e:
                    # Handle other exceptions
                    print(f"Exception: {e}")
                     
    # do stuff with message


    await asyncio.gather(
        receiveData(ws),
        sendImage(ws)
    )
                
async def startWSS():
    async with ws.serve(handleConnection, "0.0.0.0", port):
        print(f"Websocket server started on:  localhost:{port}")
        await asyncio.Future()  # run forever
