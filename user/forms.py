from django.forms import ModelForm
from . import models
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm 

class SignUpForm(UserCreationForm):
    """Form Class for SignUp form"""
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Password confirmation'})

        for fieldname in ['email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            # self.fields[fieldname].label = ""
            # self.fields[fieldname].widget.attrs['class'] = 'form-control border-0 border-bottom'

    class Meta:
        model = models.User
        fields = ["first_name", "last_name","email"]

    def clean_first_name(self, *args, **kwargs):
        """Function to validate first_name form field"""
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name must contain only alphabets.")
        if len(first_name) < 2:
            raise forms.ValidationError("First name must be at least 2 characters long.")

        return first_name