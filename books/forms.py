from django import forms
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,  Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import Accordion, AccordionGroup
from . models import *


class ExemplarForm(forms.ModelForm):
    class Meta:
        model = Exemplar
        fields = "__all__"
        widgets = {
            'related_work': autocomplete.ModelSelect2(
                url='books-ac:work-autocomplete'),
            'certainty': autocomplete.ModelSelect2(
                url='/vocabs-ac/concept-by-colleciton-ac/certainty'),
        }

    def __init__(self, *args, **kwargs):
        super(ExemplarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class ExemplarFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ExemplarFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Titel & Exemplare',
                    'related_work',
                    'related_work__title',
                    'normdata_id',
                    'certainty',
                    css_id="basic_search_fields"
                    ),
                )
            )


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(WorkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class WorkFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(WorkFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Titel & Exemplare',
                    'title',
                    'title_certainty',
                    css_id="basic_search_fields"
                    ),
                AccordionGroup(
                    'Autoren & Herausgeber',
                    'creator',
                    'creator__gnd_geographic_area',
                    'creator__gnd_date_of_death',
                    css_id="more"
                    ),
                )
            )


class CreatorForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CreatorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class CreatorFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(CreatorFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'name',
                'creator_certainty',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search',
                    'legacy_id',
                    'normdata_id',
                    'gnd_geographic_area',
                    'gnd_date_of_death',
                    css_id="more"
                    ),
                )
            )
