from django.conf.urls import url
from . import views

app_name = 'summaries'

urlpatterns = [
    url(
        r'^verfachbuecher/$',
        views.VerfachBuchListView.as_view(),
        name='verfachbuecher_browse'
    ),
    url(
        r'^verfachbuecher/detail/(?P<pk>[0-9]+)$',
        views.VerfachBuchDetailView.as_view(),
        name='verfachbuch_detail'
    ),
    url(
        r'^verfachbuecher/create/$',
        views.VerfachBuchCreate.as_view(),
        name='verfachbuch_create'
    ),
    url(
        r'^verfachbuecher/edit/(?P<pk>[0-9]+)$',
        views.VerfachBuchUpdate.as_view(),
        name='vverfachbuch_edit'
    ),
    url(
        r'^verfachbuecher/delete/(?P<pk>[0-9]+)$',
        views.VerfachBuchDelete.as_view(),
        name='verfachbuch_delete'),
]
