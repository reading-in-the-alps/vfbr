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


class AnmerkungenListView(GenericListView):
    model = Anmerkungen
    filter_class = AnmerkungenListFilter
    formhelper_class = AnmerkungenFilterFormHelper
    table_class = AnmerkungenTable
    init_columns = [
        'id',
        'text',
    ]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AnmerkungenListView, self).dispatch(*args, **kwargs)


class AnmerkungenDetailView(DetailView):
    model = Anmerkungen
    template_name = 'summaries/anmerkungen_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AnmerkungenDetailView, self).dispatch(*args, **kwargs)


class AnmerkungenCreate(BaseCreateView):

    model = Anmerkungen
    form_class = AnmerkungenForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AnmerkungenCreate, self).dispatch(*args, **kwargs)


class AnmerkungenUpdate(BaseUpdateView):

    model = Anmerkungen
    form_class = AnmerkungenForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AnmerkungenUpdate, self).dispatch(*args, **kwargs)


class AnmerkungenDelete(DeleteView):
    model = Anmerkungen
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('summaries:anmerkungen_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AnmerkungenDelete, self).dispatch(*args, **kwargs)

class InventoryEntryListView(GenericListView):
    model = InventoryEntry
    filter_class = InventoryEntryListFilter
    formhelper_class = InventoryEntryFilterFormHelper
    table_class = InventoryEntryTable
    init_columns = [
        'id',
        'inv_signatur',
    ]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InventoryEntryListView, self).dispatch(*args, **kwargs)


class InventoryEntryDetailView(DetailView):
    model = InventoryEntry
    template_name = 'summaries/inventory_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InventoryEntryDetailView, self).get_context_data()
        try:
            context['orig_data'] = json.loads(self.object.excel_row)
        except TypeError:
            context['orig_data'] = {}
        except ValueError:
            context['orig_data'] = {}
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InventoryEntryDetailView, self).dispatch(*args, **kwargs)


class InventoryEntryCreate(BaseCreateView):

    model = InventoryEntry
    form_class = InventoryEntryForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InventoryEntryCreate, self).dispatch(*args, **kwargs)


class InventoryEntryUpdate(BaseUpdateView):

    model = InventoryEntry
    form_class = InventoryEntryForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InventoryEntryUpdate, self).dispatch(*args, **kwargs)


class InventoryEntryDelete(DeleteView):
    model = InventoryEntry
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('summaries:inventory_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InventoryEntryDelete, self).dispatch(*args, **kwargs)
