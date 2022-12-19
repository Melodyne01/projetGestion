from django.db import models
from django import forms
from .models import Request
from django.forms import ModelForm, CharField, TextInput


#Form used to create one request
class RequestRegisration(forms.ModelForm):
    class Meta:
        model = Request
        exclude = ('created', 'uptaded')
class OrderindDeadline(forms.ModelForm):
    deadlineOrder = forms.ChoiceField()