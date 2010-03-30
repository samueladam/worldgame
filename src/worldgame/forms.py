# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Country


class CountryForm(forms.ModelForm):

    def clean_name(self):
        value = self.cleaned_data['name']
        if value.startswith('_'):
            raise forms.ValidationError(_('Name cannot start with _.'))
        return value

    class Meta:
        model = Country
        fields = ('name', 'details', 'color',)
