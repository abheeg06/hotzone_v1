from django.forms import ModelForm, TextInput
from .models import LocationDetail

class AddForm(ModelForm):
    class Meta:
        model = LocationDetail
        fields = ['name']

class SearchBox(ModelForm):
    class Meta:
        model = LocationDetail
        fields = ['name']