from django.contrib import admin
from .models import *


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


admin.site.register(Place)
admin.site.register(AlternativeName)
admin.site.register(Institution)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonPerson, PersonPersonAdmin)
