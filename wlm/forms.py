# -*- coding: utf-8 -*-

from django import forms

from wlm.models import Monument
from tinymce.widgets import TinyMCE

class MonumentForm(forms.ModelForm):
    class Meta:
        model = Monument
        widgets = {
            'coord_lat': forms.HiddenInput(),
            'coord_lon': forms.HiddenInput(),
            'extra_info': TinyMCE(),
        }

    def __init__(self, *args, **kwargs):
        super(MonumentForm,self).__init__(*args, **kwargs)
        self.fields['complex_root'].queryset = Monument.objects.filter(complex=True)

    city = forms.ChoiceField(choices=())
    street = forms.ChoiceField(choices=())
