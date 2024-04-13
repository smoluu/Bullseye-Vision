import asyncio
import websockets as ws
import json
import base64
from main import handleMessage

port = 8765

clients = set()


# Function to send data to all connected clients
async def sendData(data):
    # Convert data to JSON string
    json_data = json.dumps(data)
    # Send data to all connected clients
    for client in clients:
        await client.send(json_data)
    print(f"Sent message to clients: {data}")



# sends images of dartboard if there is clients
async def sendImage():
    while True:
        # insert dartboard image here
        with open("Backend/boardL.jpg", "rb") as image:
            image = image.read()
        image = base64.b64encode(image).decode("utf-8")
        data = {"type": "image", "content": image}

        for client in clients:
            await client.send(json.dumps(data))
        await asyncio.sleep(1)

# WebSocket connection handler
async def handleConnection(websocket, path):
    # Add the client to the set of connected clients
    clients.add(websocket)
    try:
        # Keep the connection open and handle incoming messages
        async for message in websocket:
            data = json.loads(message)
            print(f"Received message from client: {data}")

            # You can handle incoming messages here if needed
            if "message" in data and "type" in data["message"]:
                handleMessage(data["message"])

    finally:
        # Remove the client from the set of connected clients when the connection is closed
        clients.remove(websocket)


async def startWSS():
    async with ws.serve(handleConnection, "0.0.0.0", port):
        print(f"Websocket server started on:  localhost:{port}")
        await sendImage()
        await asyncio.Future()  # run forever


asyncio.run(startWSS())
