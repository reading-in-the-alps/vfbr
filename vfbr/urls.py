from django.conf.urls import url, include, handler404
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from entities.api_views import *
from vocabs import api_views
from summaries.api_views import *


router = routers.DefaultRouter()
router.register(r'geojson', GeoJsonViewSet, base_name='places')
router.register(r'metadata', api_views.MetadataViewSet)
router.register(r'skoslabels', api_views.SkosLabelViewSet)
router.register(r'skosnamespaces', api_views.SkosNamespaceViewSet)
router.register(r'skosconceptschemes', api_views.SkosConceptSchemeViewSet)
router.register(r'skoscollections', api_views.SkosCollectionViewSet)
router.register(r'skosconcepts', api_views.SkosConceptViewSet)
router.register(r'vfb', VerfachBuchViewSet)
router.register(r'vfb-entry', VfbEntryViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'institutions', InstitutionViewSet)
router.register(r'anmerkungen', AnmerkungenViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^transkribus/', include('transkribus.urls', namespace='transkribus')),
    url(r'^browsing/', include('browsing.urls', namespace='browsing')),
    url(r'^netvis/', include('netvis.urls', namespace="netvis")),
    url(r'^vocabs/', include('vocabs.urls', namespace='vocabs')),
    url(r'^summaries/', include('summaries.urls', namespace='summaries')),
    url(r'^vocabs-ac/', include('vocabs.dal_urls', namespace='vocabs-ac')),
    url(r'^entities-ac/', include('entities.dal_urls', namespace='entities-ac')),
    url(r'^entities/', include('entities.urls', namespace='entities')),
    url(r'^charts/', include('charts.urls', namespace='charts')),
    url(r'^', include('webpage.urls', namespace='webpage')),
]

handler404 = 'webpage.views.handler404'
