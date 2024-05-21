import asyncio
import websockets
import base64
import json
from datetime import datetime
from nlp import transcription_endpoint
import time

URI = "ws://ec2-52-15-178-2.us-east-2.compute.amazonaws.com/vega"
SERVER_URL = "http://localhost:8000"

async def receive_response(websocket):
    async for message in websocket:
        print("MESSAGE", message)
        try:
            print("START: ", datetime.now())
            body = json.loads(message)
            message_type = body['type']

            if message_type == "AUDIO":                
                resp_obj = json.dumps(transcription_endpoint(body, SERVER_URL))
                print("DONE TRANSCripTION: ", datetime.now())
                print("SENDING WS", resp_obj)
                await websocket.send(resp_obj)
        except json.JSONDecodeError as e:
            print("Web didn't send a json talk to saif")

async def main():    
    async with websockets.connect(URI) as websocket:        
        await websocket.send("ping")
        # Handle responses from the server
        await receive_response(websocket)

# Run the client
asyncio.get_event_loop().run_until_complete(main())