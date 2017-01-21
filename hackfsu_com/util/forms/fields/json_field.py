from django import forms
from django.core.exceptions import ValidationError
import json


class JsonField(forms.Field):
    def __init__(self, required=True, widget=None, label=None, initial=None, help_text='', error_messages=None,
                 show_hidden_initial=False, validators=[], localize=False, disabled=False, label_suffix=None,
                 dumps_clean=False):
        self.dumps_clean = dumps_clean
        super().__init__(required, widget, label, initial, help_text, error_messages, show_hidden_initial, validators,
                         localize, disabled, label_suffix)

    def clean(self, value):
        try:
            value_string = json.dumps(value)
            if self.dumps_clean:
                return value_string
            return value
        except TypeError as e:
            raise ValidationError(message=str(e))
