from django.forms import ModelForm
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password


from . import models

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

# class LoginForm(AuthenticationForm):
#     # email = forms.CharField(
#     #     label="",
#     #     widget=forms.TextInput(attrs={'class': 'form-control border border-5 border-dark mt-3 pt-3 pb-3 fs-1', 'placeholder': 'Email Address'})
#     # )
#     password = forms.CharField(
#         label="",
#         widget=forms.PasswordInput(attrs={'class': 'form-control border border-5 border-dark mt-3 pt-3 pb-3 fs-1', 'placeholder': 'Password'})
#     )

#     # def clean_email(self):
#     #     email = self.cleaned_data.get('email')
#     #     if not User.objects.filter(email=email).exists():
#     #         raise forms.ValidationError("User doesn't exists")
#     #     return email

class LoginForm(forms.Form):
    email = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control border border-5 border-dark mt-3 pt-3 pb-3 fs-1', 'placeholder': 'Email Address'})
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'class': 'form-control border border-5 border-dark mt-3 pt-3 pb-3 fs-1', 'placeholder': 'Password'})
    )

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email,password=password)

        return super(LoginForm, self).clean(*args, **kwargs)
        

    # def clean_email(self, *args, **kwargs):
    #     email = self.cleaned_data.get('email')

    #     user = models.User.objects.get(email=email)
    #     print(user.first_name)

    #     if not user:
    #         raise forms.ValidationError("User doesn't exists")

    #     return super(LoginForm, self).clean(*args, **kwargs)


    # def clean_password(self, *args, **kwargs):
    #     email = self.cleaned_data.get('email')
    #     user_password = self.cleaned_data.get('password')

    #     user = models.User.objects.filter(email=email).first()

    #     if user and not check_password(user_password, user.password):
    #         raise forms.ValidationError("Entered password is incorrect")
        
    #     return super(LoginForm, self).clean(*args, **kwargs)

            



       