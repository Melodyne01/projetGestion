from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Faction, Profile, Channel, Customer
import datetime

#Form used for the registration and updating of one account
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'is_staff']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Email'}),
        }

class AddFactionForm(forms.ModelForm):
    class Meta:
        model = Faction
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'})
        }

class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        
class LinkUserToFaction(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'faction', 'factionRole'] 

class AddChannel(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'})
        }
class AddCustomer(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'})
        }
    