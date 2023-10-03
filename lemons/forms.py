from django import forms
from .models import Yeet, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Profile additions
class ProfilePictureForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture", required=False)
    profile_bio = forms.CharField(label="Profile Bio", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Profile Biography'}))
    homepage_link = forms.CharField(label="Homepage Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Homepage Link'}), required=False)
    facebook_link = forms.CharField(label="Facebook Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Facebook Link'}), required=False)
    instagram_link =  forms.CharField(label="Instagram Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instagram Link'}), required=False)
    github_link =  forms.CharField(label="GitHub Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'GitHub Link'}), required=False)
    linkedin_link =  forms.CharField(label="LinkedIn Link", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'LinkedIn Link'}), required=False)

    class Meta:
        model= Profile
        fields = ('profile_image', 'profile_bio', 'homepage_link', 'facebook_link', 'instagram_link', 'github_link', 'linkedin_link', )

class YeetForm(forms.ModelForm):
    body = forms.CharField(required=True,
        widget=forms.widgets.Textarea(
            attrs={
            "placeholder": "Enter your yeet...",
            "class": "form-control",
            }
            ),
            label="",
        )
    
    class Meta:
        model = Yeet
        exclude = ("user", "likes", )

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=90, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=90, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    username = forms.CharField(label="", max_length=50,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), help_text='' )
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', )
