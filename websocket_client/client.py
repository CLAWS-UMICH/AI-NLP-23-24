import asyncio
import websockets
import base64
import json
from datetime import datetime
from nlp import transcription_endpoint
import time

# URI = "ws://ec2-52-15-178-2.us-east-2.compute.amazonaws.com/vega"?
URI = "ws://172.16.183.161:8000/vega"
SERVER_URL = "http://localhost:8000"

async def receive_response(websocket):
    async for message in websocket:
        # print("MESSAGE", message)
        try:            
            body = json.loads(message)
            message_type = body['type']

            if message_type == "AUDIO":                
                resp_obj = json.dumps(transcription_endpoint(body, SERVER_URL))                
                print("SENDING WS", resp_obj)
                await websocket.send(resp_obj)
        except json.JSONDecodeError as e:
            print(f"Received non-json response: {message}")

async def main():    
    while True:
        try:
            async with websockets.connect(URI) as websocket:        
                await websocket.send("ping")
                # Handle responses from the server
                await receive_response(websocket)
        except Exception as e:
            print("Error: ", e)

# Run the client
asyncio.get_event_loop().run_until_complete(main())