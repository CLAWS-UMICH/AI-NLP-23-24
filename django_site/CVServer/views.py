from django.shortcuts import render
from CVServer.lab_panel_finder import lab_ballz_finder
from CVServer.geosamples import find_rocks
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import os 
import base64
import json
import cv2
import numpy as np

# Create your views here.

IMAGE_PATH = "temp_image.jpg"
FITTED_MATRIX = np.load('./fit_raycast_matrix.npy')

@method_decorator(csrf_exempt, name='dispatch')
class BallsView(View):
    def __init__(self):
        pass
    
    def post(self, request):

        # payload = {
        #     "id": "Astronaut_001",
        #     "type": "IMAGE",
        #     "use": "PUT",
        #     "data": {
        #         "base_64_image": base64_image,
        #         "position, rotation, orientation"
        #         "text_from_VEGA": "",
        #         "command": []
        #     }
        # }

        # type, position, rotation, orientation

        try:
            incoming_message = json.loads(request.body)
        except Exception as e:        
            return JsonResponse({"error": e}, status=400)
        

        base_64_image = incoming_message['data']['base_64_image']

        # Decode the base64 string
        image_data = base64.b64decode(base_64_image)

        # Write the binary data to a file
        with open(IMAGE_PATH, "wb") as image_file:
            image_file.write(image_data)
        
        img_wide = cv2.imread(IMAGE_PATH)
        img = cv2.resize(img_wide, (1200, 1200))

        print("Starting LAB classifier pipeline...")
        points = lab_ballz_finder(img)

        temp = []
        for x,y in points:
            transform = np.dot(np.array([x,y,1]), FITTED_MATRIX)
            coords = f"{transform[0]},{transform[1]}"
            temp.append(coords)

        return JsonResponse({"points": temp})

@method_decorator(csrf_exempt, name='dispatch')
class RockView(View):
    def __init__(self):
        pass
    
    def post(self, request):

        # payload = {
        #     "id": "Astronaut_001",
        #     "type": "IMAGE",
        #     "use": "PUT",
        #     "data": {
        #         "base_64_image": base64_image,
        #         "position, rotation, orientation"
        #         "text_from_VEGA": "",
        #         "command": []
        #     }
        # }

        # type, position, rotation, orientation

        try:
            incoming_message = json.loads(request.body)
        except Exception as e:        
            return JsonResponse({"error": e}, status=400)

        base_64_image = incoming_message['data']['base_64_image']

        # Decode the base64 string
        image_data = base64.b64decode(base_64_image)

        # Write the binary data to a file
        with open(IMAGE_PATH, "wb") as image_file:
            image_file.write(image_data)
        
        img_wide = cv2.imread(IMAGE_PATH)
        img = cv2.resize(img_wide, (1200, 1200))

        print("Starting Rock classifier pipeline...")
        points, label = find_rocks(img)
        temp = []
        for x,y in points:
            transform = np.dot(np.array([x,y,1]), FITTED_MATRIX)
            coords = f"{transform[0]},{transform[1]}"
            temp.append(coords)

        return JsonResponse({"points": temp, "label": label})
