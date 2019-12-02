from dal import autocomplete
from django.db.models import Q
from . models import *


class WorkAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Work.objects.all()

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        return qs
