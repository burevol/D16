from django.urls import path

from .views import AdvertsView, AdvertDetailView, MyAdvertsView, AdvertCreateView, AdvertUpdateView, AdvertDeleteView, \
    AddResponseView, SendMassEmail

urlpatterns = [
    path('adverts/', AdvertsView.as_view(), name='posts'),
    path('advert/<int:pk>/', AdvertDetailView.as_view(), name='advert'),
    path('my_adverts/', MyAdvertsView.as_view(), name='my_adverts'),
    path('advert_create/', AdvertCreateView.as_view(), name='advert_create'),
    path('advert_update/<int:pk>/', AdvertUpdateView.as_view(), name='advert_update'),
    path('advert_delete/<int:pk>/', AdvertDeleteView.as_view(), name='advert_delete'),
    path('response_add/<int:pk>', AddResponseView.as_view(), name='response_add'),
    path('send_mass_email', SendMassEmail.as_view(), name='send_mass_email'),
]
