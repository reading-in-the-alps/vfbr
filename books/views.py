from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

from browsing.browsing_utils import GenericListView, BaseCreateView, BaseUpdateView

from . filters import *
from . forms import *
from . tables import *
from . models import *


class ExemplarListView(GenericListView):
    model = Exemplar
    filter_class = ExemplarListFilter
    formhelper_class = ExemplarFilterFormHelper
    table_class = ExemplarTable
    init_columns = [
        'id',
        'title',
    ]
    enable_merge = True


class ExemplarDetailView(DetailView):
    model = Exemplar
    template_name = 'books/exemplar_detail.html'


class ExemplarCreate(BaseCreateView):

    model = Exemplar
    form_class = ExemplarForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExemplarCreate, self).dispatch(*args, **kwargs)


class ExemplarUpdate(BaseUpdateView):

    model = Exemplar
    form_class = ExemplarForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExemplarUpdate, self).dispatch(*args, **kwargs)


class ExemplarDelete(DeleteView):
    model = Exemplar
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('books:exemplar_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExemplarDelete, self).dispatch(*args, **kwargs)


class WorkListView(GenericListView):
    model = Work
    filter_class = WorkListFilter
    formhelper_class = WorkFilterFormHelper
    table_class = WorkTable
    init_columns = [
        'id',
        'title',
        'creator'
    ]
    enable_merge = True


class WorkDetailView(DetailView):
    model = Work
    template_name = 'books/work_detail.html'


class WorkCreate(BaseCreateView):

    model = Work
    form_class = WorkForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WorkCreate, self).dispatch(*args, **kwargs)


class WorkUpdate(BaseUpdateView):

    model = Work
    form_class = WorkForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WorkUpdate, self).dispatch(*args, **kwargs)


class WorkDelete(DeleteView):
    model = Work
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('books:work_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WorkDelete, self).dispatch(*args, **kwargs)


class CreatorListView(GenericListView):
    model = Creator
    filter_class = CreatorListFilter
    formhelper_class = CreatorFilterFormHelper
    table_class = CreatorTable
    init_columns = [
        'id',
        'name',
        'gnd_date_of_death',
        'gnd_geographic_area',
    ]
    enable_merge = True


class CreatorDetailView(DetailView):
    model = Creator
    template_name = 'books/creator_detail.html'


class CreatorCreate(BaseCreateView):

    model = Creator
    form_class = CreatorForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreatorCreate, self).dispatch(*args, **kwargs)


class CreatorUpdate(BaseUpdateView):

    model = Creator
    form_class = CreatorForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreatorUpdate, self).dispatch(*args, **kwargs)


class CreatorDelete(DeleteView):
    model = Creator
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('books:creator_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreatorDelete, self).dispatch(*args, **kwargs)
