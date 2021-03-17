from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
# RestFramework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from encuestas_hal.local_settings import TOKEN, URL, CHAT_ID
# Models
from .models import *
# Logger
import logging
# Tools
import json
# Telegram Bot
import telegram
from telegram import Update
from telegram.ext import (
    Updater,
    PicklePersistence,
    CommandHandler,
    MessageHandler, 
    Filters,
    CallbackContext,
)

# Get an instance of a logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# bot = telegram.Bot(token=TOKEN)
# print(bot.get_me())

def start(update, context):
    message = context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Seleccion alguna de las siguientes opciones:',
        reply_markup=telegram.ReplyKeyboardMarkup(
            keyboard=[
                [
                    telegram.KeyboardButton(text='Opcion 1'), 
                    telegram.KeyboardButton(text='Opcion 2'),
                ],
            ]
        ))
    print(message)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))

def echo(update, context):
    message = update.message

    # Validando si la respuesta existe dentro de las respuestas cargadas

    
    MessageBot.objects.create(
        message_id=message.message_id,
        message=message.text,
        chat_id=message.chat.id, 
        from_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    message = context.bot.send_message(chat_id=update.effective_chat.id, text=message.text, reply_to_message_id=message.message_id)
    MessageBot.objects.create(
        message_id=message.message_id, 
        message=message.text,
        chat_id=message.chat.id, 
        from_id=message.from_user.id,
        first_name=message.from_user.first_name,
    )

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    message = context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
    print(message)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

updater.start_polling()

# API Views
class WebhookAPIView(APIView):
    """ Recibe el objeto Update enviado por telegram y procesa la data para regresar la respuesta correcta. """
    def post(self, request, *args, **kwargs):
        updates = request.body
        data = json.loads(updates)
        print(data)
        send_message_bot('Esta vivo')
        return Response(json.loads('{"message": "Se registro el link"}'), status=status.HTTP_200_OK)


# Para realizar la busqueda de la pregunta siguiente, realizaremos un getUpdates para obtener la ultima pregunta 
# enviada por el usuario, la recibe el webhook y 
class StarQuizView(View):
    def get(self, request):
        context = {}
        context["questions"] = Question.objects.all()
        
        return render(request, 'start_quiz.html', context)

    def post(self, request, *args, **kwargs):
        question = request.POST['question']
        send_message_bot(question)
        return HttpResponse(status=200)