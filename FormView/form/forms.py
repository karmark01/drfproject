from django import forms
from django.views.generic.edit import FormView

class ContactForm(forms.Form):
    name = forms.CharField()
    surname = forms.EmailField()
    msg     = forms.CharField(widget=forms.Textarea)
