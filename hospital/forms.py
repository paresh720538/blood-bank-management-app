
from django import forms
from .models import hospitalRegister
from django.forms.widgets import PasswordInput,TextInput
from django.contrib.auth.forms import AuthenticationForm


class HospitalUserForm(forms.ModelForm):
    class Meta:
        model=hospitalRegister
        fields=['username','password','email','hospital_registrationnumber','pincode','address']
    widgets = {
        'password': forms.PasswordInput()
        }

class HospitalLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())