from typing import Any
from accounts.models import Student
from django import forms
from django.contrib.auth.forms import UserCreationForm



class SubscriberRegForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['name','username', 'email', 'password1', 'password2','phone']
    
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={ 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone'})
    }
    def __init__(self, *args, **kwargs):
        super(SubscriberRegForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['placeholder'] = 'confirm password'


class SubscriberLoginForm(forms.Form):
    username = forms.CharField(max_length=255,
                                widget=forms.TextInput(attrs={'placeholder':'Username'})
    )
    password = forms.CharField(max_length=255,
                                widget=forms.PasswordInput(attrs={'placeholder':'Password'})
    )