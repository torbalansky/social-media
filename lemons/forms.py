from django import forms
from .models import Yeet

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
        exclude = ("user",)