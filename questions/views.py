from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
# RestFramework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .test_bot import *
# Models
from .models import *
# Logger
import logging
# Tools
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# API Views
class WebhookAPIView(APIView):
    """ Recibe el objeto Update enviado por telegram y procesa la data para regresar la respuesta correcta. """
    def post(self, request, *args, **kwargs):
        updates = request.body
        data = json.loads(updates)
        print(data)
        return Response(json.loads('{"message": "Se registro el link"}'), status=status.HTTP_200_OK)


class StarQuizView(View):
    def get(self, request):
        context = {}
        context["questions"] = Question.objects.all()
        
        return render(request, 'start_quiz.html', context)

    def post(self, request, *args, **kwargs):
        question = request.POST['question']
        send_message_bot(question)
        return HttpResponse(status=200)