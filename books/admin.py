from django.contrib import admin
from .models import *


class WorkAdmin(admin.ModelAdmin):
    list_display = [
        'legacy_id',
        'title',
    ]


class CreatorAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'creator_certainty',
        'normdata_id',
    ]


class ExemplarAdmin(admin.ModelAdmin):
    list_display = [
        'normdata_id',
    ]


admin.site.register(Creator, CreatorAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(Exemplar, ExemplarAdmin)
