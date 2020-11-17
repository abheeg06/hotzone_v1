from django.forms import ModelForm, TextInput
from .models import VisitedLocationDetail, LocationDetail

class AddForm(ModelForm):
    class Meta:
        model = VisitedLocationDetail
        fields = ['name']

class SearchBox(ModelForm):
    class Meta:
        model = LocationDetail
        fields = ['name']