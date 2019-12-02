from django.conf.urls import url
from . import views
from . import dal_views
from . models import *

app_name = 'vocabs'

urlpatterns = [
    url(
        r'^work-autocomplete/$', dal_views.WorkAC.as_view(
            model=Work),
        name='work-autocomplete',
    ),
]
