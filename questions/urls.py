from django.urls import path

# Views
from .views import *

urlpatterns = [
    path('webhook_1775807081/', WebhookAPIView.as_view(), name='webhook'),
    path('start_quiz/', StarQuizView.as_view(), name='start_quiz'),
]