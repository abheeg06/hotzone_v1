from django.forms import ModelForm, TextInput
from .models import VisitedLocationDetail, LocationDetail

from .models import UserDetail



class AddForm(ModelForm):
    class Meta:
        model = VisitedLocationDetail
        fields = ['name']

class SearchBox(ModelForm):
    class Meta:
        model = LocationDetail
        fields = ['name']

#wu xianzhe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']