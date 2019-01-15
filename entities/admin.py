from django.contrib import admin
from .models import *
from reversion.admin import VersionAdmin


class PersonAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'forename',
        'written_name',
    ]


class PersonPersonAdmin(admin.ModelAdmin):
    list_display = [
        'source',
        'rel_type',
        'target',
    ]


admin.site.register(Place, VersionAdmin)
admin.site.register(AlternativeName, VersionAdmin)
admin.site.register(Institution, VersionAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonPerson, PersonPersonAdmin)
