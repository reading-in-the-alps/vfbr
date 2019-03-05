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
        name='verfachbuch_edit'
    ),
    url(
        r'^verfachbuecher/delete/(?P<pk>[0-9]+)$',
        views.VerfachBuchDelete.as_view(),
        name='verfachbuch_delete'),
    url(
        r'^verfachbucheintraege/$',
        views.VfbEntryListView.as_view(),
        name='verfachbucheintrag_browse'
    ),
    url(
        r'^verfachbucheintraege/detail/(?P<pk>[0-9]+)$',
        views.VfbEntryDetailView.as_view(),
        name='verfachbucheintrag_detail'
    ),
    url(
        r'^verfachbucheintraege/create/$',
        views.VfbEntryCreate.as_view(),
        name='verfachbucheintrag_create'
    ),
    url(
        r'^verfachbucheintraege/edit/(?P<pk>[0-9]+)$',
        views.VfbEntryUpdate.as_view(),
        name='verfachbucheintrag_edit'
    ),
    url(
        r'^verfachbucheintraege/delete/(?P<pk>[0-9]+)$',
        views.VfbEntryDelete.as_view(),
        name='verfachbucheintrag_delete'
    ),
]
