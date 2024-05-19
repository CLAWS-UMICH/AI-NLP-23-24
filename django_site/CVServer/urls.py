from django.urls import path
from .views import BallsView, RockView # Import the WebhookView class

urlpatterns = [
    path('balls/', BallsView.as_view(), name='balls'),    
    path('rocks/', RockView.as_view(), name='rocks'),    
]
