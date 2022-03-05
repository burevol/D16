from django_filters import FilterSet, ModelChoiceFilter

from .models import Response, Advert


def adverts(request):
    if request is None:
        return Advert.objects.none()
    user = request.user
    return user.advert_set.all()


class ResponseFilter(FilterSet):
    post = ModelChoiceFilter(field_name='post', queryset=adverts)

    class Meta:
        model = Response
        fields = ['post']
