from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
# Bot Credentials
from encuestas_hal.settings import TOKEN, URL, CHAT_ID, BOT_ID
# Models
from .models import *
# Logger
import logging
# Tools
import json
# Telegram Bot
from telegram import (
    Update,
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    Updater,
    PicklePersistence,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

# Configuracion basica del logger para la libreria del API
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)



def send_response(context: CallbackContext, chat_id: int, text: str, reply_to_message_id: int, replay_markup: ReplyKeyboardMarkup) -> Message:
    """ Funcion encargada de construir y enviar un mensaje al usuario. """
    return context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=replay_markup,
        reply_to_message_id=reply_to_message_id
    )



def create_replay_markup(options: KeyboardButton) -> ReplyKeyboardMarkup:
    """ Funcion encargada de crear el replay_markup para el envio de respuestas. """
    return ReplyKeyboardMarkup(
        keyboard=[
            options
    ])



def chose_response(update: Update, context: CallbackContext, next_question: Question) -> MessageBot:
    """ Seleccion el tipo de pregunta (con opciones o abierta) 
        y registra la respuesta enviada para poder reporting. """
    if next_question.is_text_question:
        message = send_response(context, update.message.chat.id, next_question.question, update.message.message_id, None)
    else:
        response_queryset = Response.objects.filter(parent_question=next_question)
        options = [ KeyboardButton(text=option.response) for option in response_queryset ]
        replay_markup = create_replay_markup(options)
        message = send_response(context, update.message.chat.id, next_question.question, update.message.message_id, replay_markup)

    return MessageBot.objects.create(
        message_id=message.message_id,
        message=message.text,
        chat_id=message.chat.id, 
        from_id=message.from_user.id,
        first_name=message.from_user.first_name,
    )



def get_next_question(response: str, current_question: Question) -> Question:
    """ Regresa la siguiente pregunta del flujo en caso de existir. """
    if current_question.is_text_question:
        return current_question.next_question
    else:
        response = Response.objects.filter(response=response, parent_question=current_question)
        if response.exists():
            response = response.first()
            return response.next_question
    return None



def question_exists(chat_id: int) -> Question:
    """ Realiza una busqueda de cada una de las respuestas registradas que ha dado el bot
        y regresa la más reciente que indica es la ultima pregunta realizada por él. """
    message = MessageBot.objects.filter(chat_id=chat_id, from_id=BOT_ID).first()
    question = Question.objects.filter(question=message.message)
    if question.exists():
        return question.first()
    return None



def start(update: Update, context: CallbackContext) -> MessageBot:
    """ Funcion que define el comportamiento del bot al escribir el comando: /scrip """
    init_question = Question.objects.get(is_first_question=True)
    return chose_response(update, context, init_question)



def echo(update: Update, context: CallbackContext) -> None:
    """ Funcion que define el comportamiento que tendra el bot cuando el usuario ingrese algo diferente a
        algun comando conocido. """
    question = question_exists(update.message.chat.id)
    
    if question:
        MessageBot.objects.create(
            message_id=update.message.message_id,
            message=update.message.text,
            reply_to_message_id=question.id,
            chat_id=update.message.chat.id, 
            from_id=update.message.from_user.id,
            first_name=update.message.from_user.first_name,
            last_name=update.message.from_user.last_name,
        )

        # Validando si la respuesta existe dentro de las respuestas cargadas
        next_question = get_next_question(update.message.text, question)
        if next_question:
            chose_response(update, context, next_question)
    else:
        send_response(context, update.message.chat.id, 'Existe algun problema en el flujo de preguntas por favor contacta tú proveedor.', update.message.message_id, None)


# Configuracion e inicializacion del bot:
# https://github.com/eternnoir/pyTelegramBotAPI

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()