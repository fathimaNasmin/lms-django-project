from django.forms import ModelForm, inlineformset_factory,BaseInlineFormSet
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from .models import Question, QuizOption

from instructor.models import Category,Requirement, WhatYouWillLearn, Lesson, Course,Video


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
        if price is None or price < 0:
            raise ValidationError("Price of the course should be a greater than 0")
        
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
    parent_model=Course, model=Requirement, form=RequirementForm, formset=CustomInlineFormSet, extra=3, can_delete=True, can_delete_extra=True)

WhatYouWillLearnFormSet = inlineformset_factory(
    parent_model=Course, model=WhatYouWillLearn, form=WhatYouWillLearnForm, formset=CustomInlineFormSet, extra=3, can_delete=True, can_delete_extra=True)


# Django model form to create new course
class AddLessonForm(forms.ModelForm):
    """Form to create/add lesson to a course"""
    class Meta:
        model = Lesson
        fields = "__all__"
        exclude = ('course',)

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 8:
            raise ValidationError("Name of Lesson should have atleast 8 characters")
        return name


# Form to add lesson to the course
class VideoLearnForm(forms.ModelForm):
    """form to add extra field for video"""
    title = forms.CharField(label="",
                             widget=forms.TextInput(attrs={'placeholder': 'Video Title',
                                                           'class': 'd-inline-block w-75'}))
    video_file = forms.FileField()

    class Meta:
        model = Video
        fields = ('title', 'video_file',)
        
# define a formset for video for a lesson
VideoFormSet = inlineformset_factory(
    parent_model=Lesson, model=Video, form=VideoLearnForm, formset=CustomInlineFormSet, extra=5, can_delete=True, can_delete_extra=True)


# ===========================QUIZ FORMS==========================

# Custom form validation for 'option' by inheriting BaseInlineFormSet
class QuizOptionCustomInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        count = 0
        for form in self.forms:
            for field in form.changed_data:
                if field == 'is_answer':
                    value = form.cleaned_data[field]
                    if value:
                        count += 1
        print("count:", count)
                
        if count != 1:
            raise forms.ValidationError(
                "Only one answer can be selected.")
        

# Model Form for Question
class QuestionForm(forms.ModelForm):
    """Form for Question"""
    class Meta:
        model = Question
        fields = "__all__"
        exclude = ('course',)
        
    def clean_question_text(self):
        question_text = self.cleaned_data['question_text']
        if len(question_text) < 0:
            raise ValidationError("question can't be blank")
        return question_text
    
    
# Form for options for questions
class OptionForm(forms.ModelForm):
    """Form for options for questions"""
    
    option = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'placeholder': 'Option',
                                                          'class': 'd-inline-block w-75'}))
    is_answer = forms.BooleanField(label="is_answer", required=False, widget=forms.CheckboxInput())
    class Meta:
        model = QuizOption
        fields = "__all__"
        exclude = ('question_id',)
    

# define a formset for options for question
QuizOptionFormSet = inlineformset_factory(
    parent_model=Question, model=QuizOption, form=OptionForm, formset=QuizOptionCustomInlineFormSet, extra=4, can_delete=False)
