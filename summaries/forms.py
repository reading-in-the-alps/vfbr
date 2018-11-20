from django import forms
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import *

from . models import *


class VfbEntryForm(forms.ModelForm):
    class Meta:
        model = VfbEntry
        fields = "__all__"


class VfbEntryFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(VfbEntryFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'entry_signatur',
                    'located_in__year',
                    'adm_action_type',
                    css_id="basic_search_fields"
                    ),
                )
            )


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
                    'signatur',
                    'year',
                    css_id="basic_search_fields"
                    ),
                )
            )
