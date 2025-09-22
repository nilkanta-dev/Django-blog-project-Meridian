
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from core.models import Post
from django_bleach.forms import BleachField
from tinymce.widgets import TinyMCE
from .validators import validate_username






class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        validators=[validate_username],
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'bg-black w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'bg-black w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Email'
        })
    )
    password1 = forms.CharField(
        
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'bg-black w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Password',
            'id':'password1'
        })
    )
    password2 = forms.CharField(
        
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'bg-black w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Confirm Password',
            'id':'password2'
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class SignInForm(AuthenticationForm):
    username = UsernameField(
        max_length=150,
        validators=[validate_username],
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'bg-black w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'bg-black w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Password',
            'id':'password'
        })
    )




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'slug','is_published','is_featured']
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the content field to use BleachField form field explicitly
        self.fields['content'] = BleachField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

