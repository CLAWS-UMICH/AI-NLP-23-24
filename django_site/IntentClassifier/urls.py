from django.urls import path
from .views import WebhookView, TranscriptionView # Import the WebhookView class

urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='webhook'),
    path('transcription/', TranscriptionView.as_view(), name='transcription'),
]
