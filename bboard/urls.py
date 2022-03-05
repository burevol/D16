from django.urls import path

from .views import AdvertsView, AdvertDetailView, MyAdvertsView, AdvertCreateView, AdvertUpdateView, AdvertDeleteView, \
    AddResponseView, SendMassEmail, AdvertsCategoryListView, AdvertsCategoryView, accept_response, ResponceDeleteView, \
    MyResponsesView

urlpatterns = [
    path('categories/', AdvertsCategoryListView.as_view(), name='categories'),
    path('adverts/', AdvertsView.as_view(), name='adverts'),
    path('adverts/<str:code>', AdvertsCategoryView.as_view(), name='adverts'),
    path('advert/<int:pk>/', AdvertDetailView.as_view(), name='advert'),
    path('my_adverts/', MyAdvertsView.as_view(), name='my_adverts'),
    path('advert_create/', AdvertCreateView.as_view(), name='advert_create'),
    path('advert_update/<int:pk>/', AdvertUpdateView.as_view(), name='advert_update'),
    path('advert_delete/<int:pk>/', AdvertDeleteView.as_view(), name='advert_delete'),
    path('response_delete/<int:pk>', ResponceDeleteView.as_view(), name='response_delete'),
    path('response_add/<int:pk>', AddResponseView.as_view(), name='response_add'),
    path('send_mass_email/', SendMassEmail.as_view(), name='send_mass_email'),
    path('accept_response/<int:pk>', accept_response, name='accept_response'),
    path('my_responses', MyResponsesView.as_view(), name='my_responses')
]
