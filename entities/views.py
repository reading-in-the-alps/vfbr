from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

from browsing.browsing_utils import GenericListView, BaseCreateView, BaseUpdateView

from . filters import *
from . forms import *
from . tables import *
from . models import *
from . utils import Levenshtein


class PersonPersonListView(GenericListView):
    model = PersonPerson
    filter_class = PersonPersonListFilter
    formhelper_class = PersonPersonFilterFormHelper
    table_class = PersonPersonTable
    init_columns = [
        'id',
        'source',
        'rel_type',
        'target',
    ]
    enable_merge = True


class PersonPersonDetailView(DetailView):
    model = PersonPerson
    template_name = 'entities/personperson_detail.html'


class PersonPersonCreate(BaseCreateView):

    model = PersonPerson
    form_class = PersonPersonForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonPersonCreate, self).dispatch(*args, **kwargs)


class PersonPersonUpdate(BaseUpdateView):

    model = PersonPerson
    form_class = PersonPersonForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonPersonUpdate, self).dispatch(*args, **kwargs)


class PersonPersonDelete(DeleteView):
    model = PersonPerson
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('entities:personperson_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonPersonDelete, self).dispatch(*args, **kwargs)


class PersonListView(GenericListView):
    model = Person
    filter_class = PersonListFilter
    formhelper_class = PersonFilterFormHelper
    table_class = PersonTable
    init_columns = [
        'id',
        'written_name',
    ]
    enable_merge = True


class PersonDetailView(DetailView):
    model = Person
    template_name = 'entities/person_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            leven = int(self.request.GET.get('leven', 0))
        except ValueError:
            leven = 0
        if leven > 0 and leven < 100:
            similar = self.model.objects.annotate(
                lev_dist=Levenshtein(
                    F('written_name_leven'), self.object.written_name_leven)
                ).filter(
                    lev_dist__lte=leven
                )
            context['similar'] = similar
            context['leven'] = leven

        return context


class PersonCreate(BaseCreateView):

    model = Person
    form_class = PersonForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonCreate, self).dispatch(*args, **kwargs)


class PersonUpdate(BaseUpdateView):

    model = Person
    form_class = PersonForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonUpdate, self).dispatch(*args, **kwargs)


class PersonDelete(DeleteView):
    model = Person
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('entities:person_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonDelete, self).dispatch(*args, **kwargs)


class PlaceListView(GenericListView):
    model = Place
    filter_class = PlaceListFilter
    formhelper_class = PlaceFilterFormHelper
    table_class = PlaceTable
    init_columns = [
        'name',
        'alt_names',
        'geonames_id',
    ]


class PlaceDetailView(DetailView):
    model = Place
    template_name = 'entities/place_detail.html'


class PlaceCreate(BaseCreateView):

    model = Place
    form_class = PlaceForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlaceCreate, self).dispatch(*args, **kwargs)


class PlaceUpdate(BaseUpdateView):

    model = Place
    form_class = PlaceForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlaceUpdate, self).dispatch(*args, **kwargs)


class PlaceDelete(DeleteView):
    model = Place
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('entities:place_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlaceDelete, self).dispatch(*args, **kwargs)


class InstitutionListView(GenericListView):
    model = Institution
    filter_class = InstitutionListFilter
    formhelper_class = InstitutionFilterFormHelper
    table_class = InstitutionTable
    init_columns = [
        'written_name',
    ]


class InstitutionDetailView(DetailView):
    model = Institution
    template_name = 'entities/institution_detail.html'


class InstitutionCreate(BaseCreateView):

    model = Institution
    form_class = InstitutionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InstitutionCreate, self).dispatch(*args, **kwargs)


class InstitutionUpdate(BaseUpdateView):

    model = Institution
    form_class = InstitutionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InstitutionUpdate, self).dispatch(*args, **kwargs)


class InstitutionDelete(DeleteView):
    model = Institution
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('entities:institution_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InstitutionDelete, self).dispatch(*args, **kwargs)
