from django.urls import path
from .views import WebhookView  # Import the WebhookView class

urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='webhook'),
]
