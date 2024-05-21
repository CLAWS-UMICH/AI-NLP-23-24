# Waypoint Python Server for webosckets. It send 3 waypoints at first and then deletes 1, then loops again and again.
# Steps:
# Run this file in VSCode and AFTER run your unity scene
# Update buttons UI to these waypoints using the scroll handler provided
# Use the event system to subscribe

import asyncio
import websockets # If this gives a warning/error, open command line and do 'pip install websockets'
import base64
import cv2
import matplotlib.pyplot as plt
import colorspacious as cs
import numpy as np
from lab_panel_finder import find_balls
from geosamples import find_rocks

FITTED_MATRIX = np.load('../FittingRaycast/fit_raycast_matrix.npy')

def lab_ballz_finder(img):
    # UIA:x,y,z:a,b,c,d:$x,y$x,y$x,y$x,y

    balls = find_balls(img)            
    # balls = None
    if not balls:
        # balls = [[300,300], [300,500], [600,300], [600,500]]
        balls = [[200,300], [200, 600], [500,300], [500,600]]
    # print(balls)
    for ball in balls:
        cv2.circle(img, ball, 10, (255,0,0))
    cv2.imwrite('image.jpg', img)    
    return balls    

def geosample_identifier(img):
    return find_rocks(img)

async def handle_client(websocket, path):    
    try:    
        print("Starting Connection...")        
        while True:
            encoded_image = await websocket.recv()
            coordinates, raw_data = encoded_image.split("}$#EndHeadCoord", 1)
            img_data = base64.b64decode(raw_data)    
            with open("image.jpg",'wb+') as f:
                f.write(img_data)
            img_wide = cv2.imread('image.jpg')
            img = cv2.resize(img_wide, (1200, 1200))

            # Parse rotation vector and add location vector of classified point within POV            
            type, position, rotation, orientation = coordinates.replace("(","").replace(")","").split(":")                        
            description = ""

            if type == "UIA":
                points = lab_ballz_finder(img)             
            elif type == "geosample":
                points, description = geosample_identifier(img)
            elif type == "calibrate":
                loop = asyncio.get_event_loop()
                while True:
                    print("Enter initial test coordinates -> x,y: ", end="")
                    user_input = await loop.run_in_executor(None, input)
                    if user_input.lower() == "stop" or user_input.lower() == "quit":
                        break      
                    coords = user_input.split(",")
                    cv2.circle(img, (int(coords[0]), int(coords[1])), 10, (255,0,0))
                    cv2.imwrite('image.jpg',img)

                    while True:
                        print("Enter coordinates (type 'stop' or 'quit' to exit): ", end="")                                        
                        user_input = await loop.run_in_executor(None, input)            

                        if user_input.lower() == "stop" or user_input.lower() == "quit":
                            break                    

                        res = f"{type}:{position}:{orientation}:{user_input}:{description}"
                        await websocket.send(res)
            
            if type != "calibrate":
                # OLD HARDCODED SHIFTING
                # # Pos shift goes up or right, stretch x,y
                # X_STRETCH, Y_STRETCH = 1.8, 1.8
                # X_SHIFT, Y_SHIFT = 200, -600
                # for x,y in points:                                              
                #     new_x = (x-600)*X_STRETCH+600+X_SHIFT
                #     new_y = (y-300)*Y_STRETCH+300+Y_SHIFT

                #     coords = f"{new_x},{new_y}"
                #     temp.append(coords)
                
                temp = []
                for x,y in points:
                    transform = np.dot(np.array([x,y,1]), FITTED_MATRIX)
                    coords = f"{transform[0]},{transform[1]}"
                    temp.append(coords)

                transformed_points = "$".join(temp)

                res = f"{type}:{position}:{orientation}:{transformed_points}:{description}"            
                print(f"Sending Res: {res}")
                await websocket.send(res)            
            
    except websockets.exceptions.ConnectionClosed:
        print("Closed")


print("Listening...")
# start_server = websockets.serve(handle_client, "35.3.205.44", 5001)
start_server = websockets.serve(handle_client, "35.3.", 5001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

