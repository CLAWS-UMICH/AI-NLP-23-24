import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from IntentClassifier.utils import ExternalServiceClient
from .utils import ExternalServiceClient
import os 
import base64
import whisper
import json


BYPASS_RASA_TESTING = False
MP3_PATH = "temp_audio.mp3"
RASA_ENDPOINT = 'http://0.0.0.0:5005/webhooks/rest/webhook/'
LLM_ENDPOINT = "http://192.168.1.160:1234/v1/"

@method_decorator(csrf_exempt, name='dispatch')
class TranscriptionView(View):
    def __init__(self):
        self.model = whisper.load_model("base")
        # result = model.transcribe("test.mp3")
        # print(result["text"])
    
    def post(self, request):
        # Web sends to Vega:
        # {
        # "id": "[Astronaut_ID]",
        # "type": "AUDIO",
        # "use": "PUT",
        # "data": {
        #     "base_64_audio": "[base_64_encoding_of_mp3_in_string_format]",
        #     "text_from_VEGA": "",
        #     "command": []
        # }
        # }
        # print(request.body)
        try:
            incoming_message = json.loads(request.body)
        except Exception as e:        
            return JsonResponse({"error": e}, status=400)
        
        base_64_audio = incoming_message['data']['base_64_audio']

        # Decode the base64 string
        audio_data = base64.b64decode(base_64_audio)

        # Write the binary data to a file
        with open(MP3_PATH, "wb") as audio_file:
            audio_file.write(audio_data)

        # TODO: CONVERT BASE 64 Mp3 file to a local file and use the code below to transcribe and send the transcribed text

        result = self.model.transcribe(MP3_PATH)
        transcribed_text = result["text"]


        # RETURN:
        # "id": "[Astronaut_ID]",
        # "type": "AUDIO_PROCESSED",
        # "use": "PUT",
        # "data": {
        #     "base_64_audio": "",
        #     "text_from_VEGA": "[translated_text_from_mp3_to_text]",
        #     "command": [
        #     "[command_to_call]",
        #     "[parameter1]", // Parameters are only included if needed for the specific command to call
        #     "[parameter2]",
        #     "[parameter3]",
        #             ...
        #     "[parameter n]"
        #     ]
        return JsonResponse({"text_from_VEGA": transcribed_text})

@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):

    def __init__(self):
        self.prompting = ExternalServiceClient(LLM_ENDPOINT)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + "/prompts.json", "r") as f:
            self.prompts = json.load(f)

        # Assuming the Rasa server is running on the same host, on port 5005
        self.rasa_endpoint = RASA_ENDPOINT
    

    def get(self, request, *args, **kwargs):
        # This GET method is just for testing purposes
        return JsonResponse({'status': 'ok'}, status=200)
    def post(self, request):
        # Parse the incoming JSON data
        try:
            incoming_message = json.loads(request.body)
        except Exception as e:        
            return JsonResponse({"error": e}, status=400)

        voice_command = incoming_message['command'][0]
        # Prepare the payload to Rasa
        payload = {
            "sender": incoming_message.get("sender", "default"),  # You may want to specify the sender ID
            "message": voice_command
        }     
        
        # TODO: Work on messing with this so we can test out the GPT code using an endpoint 
        #       (if BYPASS_RASA_TESTING skip the Rasa processing for now)
        if not BYPASS_RASA_TESTING:
            print("Making a request to rasa webserver...")

            # Make a POST request to the Rasa server
            response = requests.post(self.rasa_endpoint, json=payload)
            print(response.json())
            classification = response.json()[0]['text'].replace("'", '"')

            # Check if the request was successful
            if response.status_code != 200:
                # Return an error response
                return JsonResponse({"error": "Error communicating with Rasa"}, status=response.status_code)    
            
            if (classification in self.prompts):                
                response = self.prompting.execute_command(voice_command, self.prompts[classification])
                return JsonResponse(response, safe=False)
            
            return JsonResponse(classification, safe=False)

        else:
            classification = voice_command
            if (classification in self.prompts):
                response = self.prompting.execute_command(voice_command, self.prompts[classification])
                return JsonResponse(response, safe=False)
            else:
                response = self.prompting.execute_command(voice_command, self.prompts['sample'])
                return JsonResponse(response, safe=False)
