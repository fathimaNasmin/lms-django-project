from django.forms import ModelForm
from django import forms
from django.core.validators import RegexValidator

from . import models

class AddCourseForm(forms.ModelForm):
    """Form to create/add course"""

    

    class Meta:
        model = models.Course
        fields = "__all__"
        exclude = ('author',)

