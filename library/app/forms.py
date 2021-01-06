from django import forms
from .models import *


class RegisterForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}
    )
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password'}
    )
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Name'
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email'
            }
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        )
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Address'
            }
        )
    )

    class Meta:
        model = User
        fields = ['name', 'username', 'password', 'address', 'email']


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'username'}
        )
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'password'}
    )
    )


class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Name'}
    ))
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}
    ))
    content = forms.CharField(max_length=2000, widget=forms.Textarea(
        attrs={'placeholder': 'Your message ...'}
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


    class Meta:
        model = Message
        fields = ['name','email','content']
