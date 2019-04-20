from django import forms
from .validators import *

class submitURL(forms.Form):
    url = forms.CharField(
        label='',
        validators=[valid],
        widget=forms.TextInput(
            attrs={'placeholder': 'Long URL',
                   'class': 'form-control'},
        )
    )

    def clean_url(self):
        url = self.cleaned_data['url']
        result=valid(url)
        return result
