from django import forms

from wlm.models import Monument, City

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
        super(MonumentForm, self).__init__(*args, **kwargs)
        qs = Monument.objects.filter(complex=True)
        self.fields['complex_root'].queryset = qs
        self.fields['city'].required = False

    city = forms.ChoiceField(choices=())
    #street = forms.ChoiceField(choices=())

    def clean_city(self):
        city = self.cleaned_data['city']
        if city:
            return City.objects.get(id=city)
        return None

    def clean_street(self):
        return None
