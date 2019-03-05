import json
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

from browsing.browsing_utils import GenericListView, BaseCreateView, BaseUpdateView

from . filters import *
from . forms import *
from . models import *
from . tables import *


class VfbEntryListView(GenericListView):
    model = VfbEntry
    filter_class = VfbEntryListFilter
    formhelper_class = VfbEntryFilterFormHelper
    table_class = VfbEntryTable
    init_columns = [
        'id',
        'located_in',
        'adm_action_type',
        'inventory',
    ]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VfbEntryListView, self).dispatch(*args, **kwargs)


class VfbEntryDetailView(DetailView):
    model = VfbEntry
    template_name = 'summaries/verfachbucheintrag_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VfbEntryDetailView, self).dispatch(*args, **kwargs)


class VfbEntryCreate(BaseCreateView):

    model = VfbEntry
    form_class = VfbEntryForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VfbEntryCreate, self).dispatch(*args, **kwargs)


class VfbEntryUpdate(BaseUpdateView):

    model = VfbEntry
    form_class = VfbEntryForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VfbEntryUpdate, self).dispatch(*args, **kwargs)


class VfbEntryDelete(DeleteView):
    model = VfbEntry
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('summaries:verfachbucheintrag_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VfbEntryDelete, self).dispatch(*args, **kwargs)


class VerfachBuchListView(GenericListView):
    model = VerfachBuch
    filter_class = VerfachBuchListFilter
    formhelper_class = VerfachBuchFilterFormHelper
    table_class = VerfachBuchTable
    init_columns = [
        'id',
        'signatur',
        'year',
    ]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VerfachBuchListView, self).dispatch(*args, **kwargs)


class VerfachBuchDetailView(DetailView):
    model = VerfachBuch
    template_name = 'summaries/verfachbuch_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VerfachBuchDetailView, self).dispatch(*args, **kwargs)


class VerfachBuchCreate(BaseCreateView):

    model = VerfachBuch
    form_class = VerfachBuchForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VerfachBuchCreate, self).dispatch(*args, **kwargs)


class VerfachBuchUpdate(BaseUpdateView):

    model = VerfachBuch
    form_class = VerfachBuchForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VerfachBuchUpdate, self).dispatch(*args, **kwargs)


class VerfachBuchDelete(DeleteView):
    model = VerfachBuch
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('summaries:verfachbuch_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VerfachBuchDelete, self).dispatch(*args, **kwargs)
