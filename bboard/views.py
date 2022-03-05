from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.views.generic.base import TemplateView

from .filters import ResponseFilter
from .forms import AdvertForm, ResponseForm, MassEmailForm
from .models import Advert, Response, User, CATEGORY


class StaffMixin(AccessMixin):
    """Verify that the current user is staff."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AdvertsCategoryListView(TemplateView):
    template_name = 'bboard/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CATEGORY
        return context


class AdvertsCategoryView(ListView):
    template_name = 'bboard/adverts.html'
    model = Advert
    paginate_by = 10

    def get_queryset(self):
        code = self.kwargs.get('code')
        return Advert.objects.filter(category=code)


class MyResponsesView(ListView):
    template_name = 'bboard/my_responses.html'
    model = Response
    paginate_by = 10

    def get_queryset(self):
        current_user = self.request.user
        return Response.objects.filter(recipient=current_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ResponseFilter(self.request.GET, request=self.request, queryset=self.get_queryset())
        return context


class AdvertsView(ListView):
    template_name = 'bboard/adverts.html'
    model = Advert
    ordering = ["-date"]
    paginate_by = 10


class AdvertDetailView(DetailView):
    template_name = 'bboard/advert.html'
    model = Advert


class AdvertCreateView(LoginRequiredMixin, CreateView):
    template_name = 'bboard/advert_create.html'
    form_class = AdvertForm
    login_url = '/accounts/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AdvertCreateView, self).form_valid(form)


class AdvertUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'bboard/advert_create.html'
    form_class = AdvertForm
    login_url = '/accounts/login/'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Advert.objects.get(pk=pk)


class MyAdvertsView(LoginRequiredMixin, ListView):
    template_name = 'bboard/my_adverts.html'
    model = Advert
    login_url = '/accounts/login/'
    paginate_by = 10

    def get_queryset(self):
        current_user = self.request.user
        return Advert.objects.filter(author=current_user)


class AdvertDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'bboard/advert_delete.html'
    queryset = Advert.objects.all()
    success_url = '/bboard/my_adverts'
    login_url = '/accounts/login/'


class ResponceDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'bboard/response_delete.html'
    queryset = Advert.objects.all()
    success_url = '/bboard/my_adverts'
    login_url = '/accounts/login/'


class AddResponseView(LoginRequiredMixin, CreateView):
    template_name = 'bboard/response_add.html'
    model = Response
    form_class = ResponseForm
    success_url = '/bboard/adverts/'
    login_url = '/accounts/login/'

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


class SendMassEmail(StaffMixin, View):
    form_class = MassEmailForm
    template_name = 'bboard/send_mass_email.html'
    login_url = '/accounts/login/'

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


def accept_response(request, pk):
    response = Response.objects.get(pk=pk)
    if response.recipient == request.user:
        send_mail(
            f'{response.sender.username}, ваш отклик подтвержден!',
            f'Отклик на объявление {response.post.header} подтвержден',
            settings.DEFAULT_FROM_EMAIL,
            [response.sender.email],
            fail_silently=False
        )
    return HttpResponseRedirect('/bboard/adverts/')
