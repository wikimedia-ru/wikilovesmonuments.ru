from django import forms
from tinymce.widgets import TinyMCE

from wlm.models import Monument, City


class MonumentForm(forms.ModelForm):
    class Meta:
        model = Monument
        widgets = {
            'coord_lat': forms.HiddenInput(),
            'coord_lon': forms.HiddenInput(),
            'extra_info': TinyMCE(),
        }

    def __init__(self, *args, **kwargs):
        super(MonumentForm, self).__init__(*args, **kwargs)
        qs = Monument.objects.filter(complex=True)
        self.fields['complex_root'].queryset = qs
        self.fields['city'].required = True

    def clean_street(self):
        return None
