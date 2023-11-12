from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):

    def get(self, request, *args, **kwargs):
        # This is just for testing purposes and should not be used in production
        return JsonResponse({'status': 'ok'}, status=200)

    def post(self, request, *args, **kwargs):
        # You can access the POST data from Rasa with request.body
        # Here you'd run some logic to handle the Rasa request
        print('response', request.body)
        return JsonResponse({'status': 'received'})
