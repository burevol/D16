from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from .forms import AdvertForm, ResponseForm, MassEmailForm
from .models import Advert, Response, User


class AdvertsView(ListView):
    template_name = 'bboard/adverts.html'
    model = Advert


class AdvertDetailView(DetailView):
    template_name = 'bboard/advert.html'
    model = Advert


class AdvertCreateView(CreateView):
    template_name = 'bboard/advert_create.html'
    form_class = AdvertForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AdvertCreateView, self).form_valid(form)


class AdvertUpdateView(UpdateView):
    template_name = 'bboard/advert_create.html'
    form_class = AdvertForm

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Advert.objects.get(pk=pk)


class MyAdvertsView(ListView):
    template_name = 'bboard/my_adverts.html'
    model = Advert

    def get_queryset(self):
        current_user = self.request.user
        return Advert.objects.filter(author=current_user)


class AdvertDeleteView(DeleteView):
    template_name = 'bboard/advert_delete.html'
    queryset = Advert.objects.all()
    success_url = '/bboard/my_adverts'


class AddResponseView(CreateView):
    template_name = 'bboard/response_add.html'
    model = Response
    form_class = ResponseForm
    success_url = '/bboard/adverts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['post'] = Advert.objects.get(pk=pk)
        return context

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        post = Advert.objects.get(pk=pk)
        form.instance.sender = self.request.user
        form.instance.recipient = post.author
        form.instance.post = post
        return super(AddResponseView, self).form_valid(form)


class SendMassEmail(View):
    form_class = MassEmailForm
    template_name = 'bboard/send_mass_email.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            text = form.cleaned_data['message_text']
            if text:
                send_mass_message(text)
        return HttpResponseRedirect('/bboard/adverts/')


# TODO организовать асинхронный вызов
def send_mass_message(text):
    user_data = User.objects.values('email', 'first_name')
    for user in user_data:
        if user['email']:
            send_mail(
                f'{user["first_name"]}, у нас есть свежие новости!',
                text,
                settings.DEFAULT_FROM_EMAIL,
                [user['email']],
                fail_silently=False
            )
