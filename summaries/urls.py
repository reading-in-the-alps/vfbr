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
    url(
        r'^anmerkungen/$',
        views.AnmerkungenListView.as_view(),
        name='anmerkungen_browse'
    ),
    url(
        r'^anmerkungen/detail/(?P<pk>[0-9]+)$',
        views.AnmerkungenDetailView.as_view(),
        name='anmerkung_detail'
    ),
    url(
        r'^anmerkungen/create/$',
        views.AnmerkungenCreate.as_view(),
        name='anmerkung_create'
    ),
    url(
        r'^anmerkungen/edit/(?P<pk>[0-9]+)$',
        views.AnmerkungenUpdate.as_view(),
        name='anmerkung_edit'
    ),
    url(
        r'^anmerkungen/delete/(?P<pk>[0-9]+)$',
        views.AnmerkungenDelete.as_view(),
        name='anmerkung_delete'),
    url(
        r'^inventory/$',
        views.InventoryEntryListView.as_view(),
        name='inventory_browse'
    ),
    url(
        r'^inventory/detail/(?P<pk>[0-9]+)$',
        views.InventoryEntryDetailView.as_view(),
        name='inventory_detail'
    ),
    url(
        r'^inventory/create/$',
        views.InventoryEntryCreate.as_view(),
        name='inventory_create'
    ),
    url(
        r'^inventory/edit/(?P<pk>[0-9]+)$',
        views.InventoryEntryUpdate.as_view(),
        name='inventory_edit'
    ),
    url(
        r'^inventory/delete/(?P<pk>[0-9]+)$',
        views.InventoryEntryDelete.as_view(),
        name='inventory_delete'
    ),
]
