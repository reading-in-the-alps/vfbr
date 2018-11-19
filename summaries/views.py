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


class VerfachBuchListView(GenericListView):
    model = VerfachBuch
    filter_class = VerfachBuchListFilter
    formhelper_class = VerfachBuchFilterFormHelper
    table_class = VerfachBuchTable
    init_columns = [
        'id',
        'title',
        'signature',
    ]


class VerfachBuchDetailView(DetailView):
    model = VerfachBuch
    template_name = 'summaries/verfachbuch_detail.html'


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
