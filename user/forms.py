from django.forms import ModelForm
from . import models
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm 
from crispy_bootstrap5.bootstrap5 import FloatingField

class SignUpForm(UserCreationForm):
    """Form Class for SignUp form"""
    def __init__(self, *args, **kwargs):

        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget = forms.TextInput(
            attrs={'placeholder': 'First Name'})

        self.fields['last_name'].widget = forms.TextInput(
            attrs={'placeholder': 'Last Name'})

        self.fields['email'].widget = forms.EmailInput(
            attrs={'placeholder': 'Email'})

        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Password'})

        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Password confirmation'})

        for fieldname in ['first_name', 'last_name', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = ""
            self.fields[fieldname].widget.attrs['class'] = 'form-control border border-5 border-dark mt-3 pt-3 pb-3 fs-1'

        

    class Meta:
        model = models.User
        fields = ["first_name", "last_name","email"]

    def clean(self, *args, **kwargs):
        """Function to validate first_name form field"""
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if not first_name.isalpha():
            raise forms.ValidationError("First name must contain only alphabets.")
        
        if not last_name.isalpha():
            raise forms.ValidationError("Last Name must contain only alphabets.")

        if (len(first_name) or len(last_name)) <= 2:
            raise forms.ValidationError("Firstname and Lastname must be at least 2 characters long.")

       