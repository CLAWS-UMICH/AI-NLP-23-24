import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):

    # Assuming the Rasa server is running on the same host, on port 5005
    # rasa_endpoint = 'http://localhost:5005/webhooks/rest/webhook/'
    rasa_endpoint = 'https://248f-35-3-93-79.ngrok-free.app/webhooks/rest/webhook/'

    def get(self, request, *args, **kwargs):
        # This GET method is just for testing purposes
        return JsonResponse({'status': 'ok'}, status=200)

    def post(self, request, *args, **kwargs):
        # Parse the incoming JSON data
        incoming_message = json.loads(request.body)

        # Prepare the payload to Rasa
        payload = {
            "sender": incoming_message.get("sender", "default"),  # You may want to specify the sender ID
            "message": incoming_message.get("message", "")
        }

        # Make a POST request to the Rasa server
        response = requests.post(self.rasa_endpoint, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Return Rasa's response
            return JsonResponse(response.json(), safe=False)
        else:
            # Return an error response
            return JsonResponse({"error": "Error communicating with Rasa"}, status=response.status_code)
