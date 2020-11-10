from django import forms
from .models import *
from tempus_dominus.widgets import DatePicker

class SearchForm(forms.Form):
    keywords = forms.CharField(label='Location', max_length=100)

class LocationVisitedForm(forms.ModelForm):

    class Meta:
        model = LocationVisited
        fields = ('name', 'address',
                    'x', 'y',
                    'date_from', 'date_to', 'catagory')
        widgets = {
            'date_from': DatePicker(),
            'date_to': DatePicker()

        }
