from django import forms
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import *

from . models import *


class VerfachBuchForm(forms.ModelForm):
    class Meta:
        model = VerfachBuch
        fields = "__all__"


class VerfachBuchFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(VerfachBuchFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'title',
                    'res_type',
                    css_id="basic_search_fields"
                    ),
                AccordionGroup(
                    'Inhalt',
                    'subject_norm',
                    'abstract',
                    css_id="more"
                    ),
                AccordionGroup(
                    'Datierung',
                    'written_date',
                    'not_before',
                    'not_after',
                    css_id="datierung"
                    ),
                AccordionGroup(
                    'Bestand',
                    'archiv',
                    'signature',
                    css_id="bestand"
                    ),
                )
            )
