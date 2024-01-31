import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from IntentClassifier.utils import ExternalServiceClient
from .utils import ExternalServiceClient

BYPASS_RASA_TESTING = False
LLAMA = False

@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):

    def __init__(self):
        self.prompting = ExternalServiceClient("")

    # Assuming the Rasa server is running on the same host, on port 5005
    rasa_endpoint = 'http://localhost:5005/webhooks/rest/webhook/'
    #rasa_endpoint = 'https://248f-35-3-93-79.ngrok-free.app/webhooks/rest/webhook/'

    def get(self, request, *args, **kwargs):
        # This GET method is just for testing purposes
        return JsonResponse({'status': 'ok'}, status=200)
    def post(self, request):
        # Parse the incoming JSON data
        incoming_message = json.loads(request.body)
        print(incoming_message['message']['command'])
        # Prepare the payload to Rasa
        payload = {
            "sender": incoming_message.get("sender", "default"),  # You may want to specify the sender ID
            "message": incoming_message['message']['command']
        }     
        
        # TODO: Work on messing with this so we can test out the GPT code using an endpoint 
        #       (if BYPASS_RASA_TESTING skip the Rasa processing for now)
        if not BYPASS_RASA_TESTING:
            # Make a POST request to the Rasa server
            response = requests.post(self.rasa_endpoint, json=payload)
            command_str = json.loads(response.text)[0]['text']
            command = json.loads('"' + command_str + '"')
            try:
                if (command == "geosample"):
                    if not (LLAMA):
                        esc = ExternalServiceClient("")    
                        indata = incoming_message['message']
                        response = esc.execute_command(indata["voice_command"], indata["tags"])
                        print(response.text)
                        return JsonResponse(json.dumps(response), safe=False)
                    else:
                        return JsonResponse({"error":"no llama integration"})
            except:
                return JsonResponse({"error":"command failed to be parsed"})
        else:
            esc = ExternalServiceClient("")    
            indata = incoming_message['message']
            response = esc.execute_command(indata["voice_command"], indata["tags"])
            return JsonResponse(json.dumps(response), safe=False)
            # filestr = f.read()
            # filestrlist = filestr.split("\n")
            # tagslist = []
            # sentencelist = []
            # for i in range(1, len(filestrlist), 2):
            #     tagslist.append(filestrlist[i].split(", "))
            #     sentencelist.append(filestrlist[i-1])

            # for i in range(1, len(sentencelist)):
            #     resp = esc.execute_command(sentencelist[i], tagslist[i])
            #     print(resp)

        # Check if the request was successful
        if response.status_code == 200:
            # Return Rasa's response
            return JsonResponse(response.json(), safe=False)
        else:
            # Return an error response
            return JsonResponse({"error": "Error communicating with Rasa"}, status=response.status_code)
        
        