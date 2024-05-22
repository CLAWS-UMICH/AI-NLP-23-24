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

from IntentClassifier.utils import ExternalServiceClient


# Create your views here.

IMAGE_PATH = "temp_image.jpg"
FITTED_MATRIX = np.load('./fit_raycast_matrix.npy')
CAPTION_ENDPOINT = "http://172.16.183.135:2345/v1/"

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

# # Example: reuse your existing OpenAI setup
# from openai import OpenAI

# FEW_SHOT_PROMPTS = """
#     Input: Record this rock that is blue and yellow 
#     Output: {"color":"blue and yellow", "location":null, "type":null}
#     Input: Geo Sampling blue lithium rock, weighs around 40 pounds
#     Output: {"color":"blue", "location":null, "type":"lithium"}
#     Input: Sample a basalt rock with a diameter of 10 inches
#     Output: {"color":null, "location":null, "type":"basalt"}
#     Input:Found basalt in Hadley Rille. 
#     Output: {"color":null, "location":"Hadley Rille", "type":"basalt"}
# """
# # Point to the local server
# client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

# completion = client.chat.completions.create(
#   model="local-model", # this field is currently unused
#   messages=[
#     {"role": "system", "content": """
#                     Given a sentence, you extract the rock color, rock location, and rock type in the following format
#                     {"color":"<color>", "location":"<location>", "type":"<type>"}
#                     Put null if the tag cannot be found in the sentence.
#                     ###EXAMPLES###
#                     """ +
#                     FEW_SHOT_PROMPTS
#                 },
#     {"role": "user", "content": "Record a pink obsidian rock found by NASA astronauts on the lunar surface"}
#   ],
#   temperature=0,
#   max_tokens=200,
# )

# print(completion.choices[0].message)

@method_decorator(csrf_exempt, name='dispatch')
class RockView(View):
    def __init__(self):
        self.prompting = ExternalServiceClient(CAPTION_ENDPOINT)
    
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
        points, label = find_rocks(img, generate_caption=True, prompting=self.prompting)
        temp = []
        for x,y in points:
            transform = np.dot(np.array([x,y,1]), FITTED_MATRIX)
            coords = f"{transform[0]},{transform[1]}"
            temp.append(coords)
        
        return JsonResponse({"points": temp, "label": label})
