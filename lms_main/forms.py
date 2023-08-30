from django.forms import ModelForm, inlineformset_factory
from django import forms
from django.core.validators import RegexValidator

from .models import Course,Category,Requirement,WhatYouWillLearn


# Django model form to create new course
class AddCourseForm(forms.ModelForm):
    """Form to create/add course"""
    class Meta:
        model = Course
        fields = "__all__"
        exclude = ('author',)

# Django model form to add Requirement fields to AddCourseForm
class RequirementForm(forms.ModelForm):
    """form to add extra field for requirements"""
    requirement_points = forms.CharField(label="",
                                         widget=forms.TextInput(attrs=
                                                                {'placeholder': 'Add Requirements here',
                                                                 'class': 'd-inline-block w-75'}))
    
    
    # def __init__(self, *args, **kwargs):
    #     super(RequirementForm, self).__init__(*args, **kwargs)
    #     self.fields['requirement_points'].label = ""
    #     self.fields['requirement_points'].placeholder = "Add Requirements here"
    class Meta:
        model = Requirement
        fields = ('requirement_points',)
        
# Django model form to add WhatYouWillLearn fields to AddCourseForm


class WhatYouWillLearnForm(forms.ModelForm):
    """form to add extra field for WhatYouWillLearn"""
    points = forms.CharField(label="",
                             widget=forms.TextInput(attrs={'placeholder': 'points',
                                                                       'class': 'd-inline-block w-75'}))
    class Meta:
        model = WhatYouWillLearn
        fields = ('points',)


RequirementFormSet = inlineformset_factory(
    parent_model=Course, model=Requirement, form=RequirementForm, extra=1, can_delete=True, can_delete_extra=True)

WhatYouWillLearnFormSet = inlineformset_factory(
    parent_model=Course, model=WhatYouWillLearn, form=WhatYouWillLearnForm, extra=3, can_delete=True, can_delete_extra=True)
