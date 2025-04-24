from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

attrs = {'class' : 'form-control'}


class UserLoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs=attrs)
    )

    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs=attrs)
    )



class UserRegisterForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs=attrs)
    )

    email = forms.CharField(
        label='email',
        widget=forms.TextInput(attrs=attrs)
    )

    first_name = forms.CharField(
        label='first_name',
        widget=forms.TextInput(attrs=attrs)
    )
    last_name = forms.CharField(
        label='last_name',
        widget=forms.TextInput(attrs=attrs)
    )
    
    password1 = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs=attrs)
    )

    password2 = forms.CharField(
        label='password confirmation',
        widget=forms.PasswordInput(attrs=attrs)
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                 'last_name', 'password1', 'password2']