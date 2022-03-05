from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm, Form, CharField, Textarea
from allauth.account.forms import SignupForm

from .models import Advert, Response


class AdvertForm(ModelForm):
    content = CharField(widget=CKEditorWidget)

    class Meta:
        model = Advert
        fields = ['header', 'content', 'category']


class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ['content']


class MassEmailForm(Form):
    message_text = CharField(max_length=512, label='Сообщение рассылки', widget=Textarea)


class CustomSignupForm(SignupForm):
    first_name = CharField(max_length=30, label='First Name')
    last_name = CharField(max_length=30, label='Last Name')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user