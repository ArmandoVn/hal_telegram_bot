from django.db import models
from django.contrib import messages
from django.core.exceptions import ValidationError

# Create your models here.
class Question(models.Model):
    """ Clase que define los atributus del modelo pregunta del bot """
    question = models.CharField(max_length=220, null=False, blank=False)
    context = models.CharField(max_length=220, null=False, blank=False)
    is_text_question = models.BooleanField(default=False)
    next_question = models.ForeignKey('self', related_name='NextQuestion', null=True, blank=True, on_delete=models.PROTECT)
    is_first_question = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=True)
    created_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.is_text_question:
            self.next_question = None
        super(Question, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

class Response(models.Model):
    """ Clase que define los atributus del modelo respuesta del bot """
    response = models.CharField(max_length=220, null=False, blank=False)
    context = models.CharField(max_length=220, null=False, blank=False)
    parent_question = models.ForeignKey('Question', related_name='ParentResponseQuestion', null=True, blank=True, on_delete=models.PROTECT)
    next_question = models.ForeignKey('Question', related_name='NextResponseQuestion', null=True, blank=True, on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    def __str__(self):
        return self.response

    def save(self, *args, **kwargs):
        if self.parent_question:
            if self.parent_question.is_text_question:
                raise ValidationError("The parent question doesn't have responses")
        super(Response, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


class MessageBot(models.Model):
    """ Clase que almacena los mensajes enviados y contestados """
    message_id = models.PositiveIntegerField(primary_key=True)
    reply_to_message_id = models.PositiveIntegerField(null=True, blank=True)
    message = models.CharField(max_length=220, null=False, blank=False)
    chat_id = models.CharField(max_length=220, null=False, blank=False)
    from_id = models.CharField(max_length=220, null=False, blank=False)
    first_name = models.CharField(max_length=220, null=False, blank=False)
    last_name = models.CharField(max_length=220, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-created_at']