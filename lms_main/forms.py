from django.forms import ModelForm, inlineformset_factory,BaseInlineFormSet
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from .models import Course,Category,Requirement,WhatYouWillLearn


# Custom form validation by inheritinf BaseInlineFormSet
class CustomInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            # your custom formset validation
            for field in form.changed_data:
                print(form.cleaned_data[field])

# Django model form to create new course
class AddCourseForm(forms.ModelForm):
    """Form to create/add course"""
    class Meta:
        model = Course
        fields = "__all__"
        exclude = ('author','slug')
        
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 8:
            raise ValidationError("Title should be greater than 8 characters")
        return title
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError("Price of the course should be a positive value")
        
    def clean_status(self):
        status = self.cleaned_data['status']
        if not status:
            raise ValidationError("Please select any one")
        return status
            

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
        
    # def clean(self):
    #     super().clean()
    #     requirement_points = self.cleaned_data.get("requirement_points")
        
        
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
    parent_model=Course, model=Requirement, form=RequirementForm, formset=CustomInlineFormSet, extra=0, can_delete=True, can_delete_extra=True)

WhatYouWillLearnFormSet = inlineformset_factory(
    parent_model=Course, model=WhatYouWillLearn, form=WhatYouWillLearnForm, formset=CustomInlineFormSet, extra=3, can_delete=True, can_delete_extra=True)


