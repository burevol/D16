from django.forms import ModelForm, Form, CharField, Textarea

from .models import Advert, Response


class AdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = ['header', 'text', 'category']


class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ['content']


class MassEmailForm(Form):
    message_text = CharField(max_length=512, label='Сообщение рассылки', widget=Textarea)
