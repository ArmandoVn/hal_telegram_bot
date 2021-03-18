from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_text_question', 'next_question', 'is_first_question',)
    search_fields = ('question',)

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('response', 'parent_question', 'next_question',)
    search_fields = ('response',)

@admin.register(MessageBot)
class MessageBotAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )
    list_display = ('message_id', 'message', 'reply_to_message_id', 'from_id', 'chat_id', 'created_at', )
    search_fields = ('message_id', 'from_id', 'chat_id', )