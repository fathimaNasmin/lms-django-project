from user.models import Student
from django.forms import ModelForm
from django import forms

class UpdateProfileForm(forms.ModelForm):
    """Form class to update profile"""
    profile_image = forms.ImageField(label="")

    class Meta:
        model = Student
        fields = ('profile_image',)
