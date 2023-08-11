from django.forms import ModelForm
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

from . import models


User = get_user_model()



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
        model = User
        fields = ["first_name", "last_name", "email"]

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


class LoginForm(AuthenticationForm):
    """Custom Login Form inherit the Authentication form for authenticating the user"""
    username = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'autofocus': True,'class': 'form-control border border-5 border-dark mt-3 pt-3 pb-3 fs-1', 'placeholder': 'Email'}),
    )

    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'class': 'form-control border border-5 border-dark mt-3 pt-3 pb-3 fs-1', 'placeholder': 'Password'})
    )

    class Meta:
        model = User
        fields = ["email", "password"]

    
    def clean(self):
        """form validation using clean() method"""
        email = self.cleaned_data['username']
        password = self.cleaned_data['password']

        try:
            user = User.objects.filter(email=email, student__isnull=False).exists()

        except User.DoesNotExist:
            user = None
            student = None
            
        else:
            if user:
                user_pass = User.objects.get(email=email)
                if user_pass.check_password(password):
                    # print("correct password")
                    pass
                else:
                    raise forms.ValidationError("Incorrect email or password")
            else:
                # print("Student doesn't exists")
                raise forms.ValidationError("Student doesn't exists")
        finally:
            # print("done validation in final block")
            pass
        
        
        
class InstructorLoginForm(AuthenticationForm):
    """Custom Login Form inherit the Authentication form for authenticating the user"""
    username = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'autofocus': True,'class': 'form-control border border-5 border-dark mt-3 pt-3 pb-3 fs-1', 'placeholder': 'Email'}),
    )

    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'class': 'form-control border border-5 border-dark mt-3 pt-3 pb-3 fs-1', 'placeholder': 'Password'})
    )

    class Meta:
        model = User
        fields = ["email", "password"]

    
    def clean(self):
        """form validation using clean() method"""
        email = self.cleaned_data['username']
        password = self.cleaned_data['password']

        try:
            user = User.objects.filter(email=email, instructor__isnull=False).exists()

        except User.DoesNotExist:
            user = None
            student = None
            
        else:
            if user:
                user_pass = User.objects.get(email=email)
                if user_pass.check_password(password):
                    # print("correct password")
                    pass
                else:
                    raise forms.ValidationError("Incorrect email or password")
            else:
                # print("Instructor doesn't exists")
                raise forms.ValidationError("Instructor doesn't exists")
        finally:
            print("done validation in final block")
            pass

    