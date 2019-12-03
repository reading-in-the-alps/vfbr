from django.conf.urls import url
from . import views
from . import dal_views
from .models import *

app_name = 'vocabs'

urlpatterns = [
    url(
        r'^altname-autocomplete/$', dal_views.AlternativeNameAC.as_view(
            model=AlternativeName, create_field='name',),
        name='altname-autocomplete',
    ),
    url(
        r'^place-autocomplete/$', dal_views.PlaceAC.as_view(
            model=Place, create_field='name',),
        name='place-autocomplete',
    ),
    url(
        r'^person-autocomplete/$', dal_views.PersonAC.as_view(
            model=Place, create_field='name',),
        name='person-autocomplete',
    ),
    url(
        r'^main-person-autocomplete/$', dal_views.MainPersonAC.as_view(),
        name='main-person-autocomplete',
    ),
    url(
        r'^adm-person-autocomplete/$', dal_views.AdmPersonAC.as_view(),
        name='adm-person-autocomplete',
    ),
    url(
        r'^rel-person-autocomplete/$', dal_views.RelPersonAC.as_view(),
        name='rel-person-autocomplete',
    ),
    url(
        r'^other-person-autocomplete/$', dal_views.OtherPersonAC.as_view(),
        name='other-person-autocomplete',
    ),
    url(
        r'^institution-autocomplete/$', dal_views.InstitutionAC.as_view(
            model=Institution, create_field='written_name',),
        name='institution-autocomplete',
    ),
]
