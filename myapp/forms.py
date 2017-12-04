from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    in_game_id = forms.CharField(max_length=30, required=True, help_text='Required. Max 30 Characters')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    # account_id = forms.IntegerField(widget=forms.HiddenInput())
    # summoner_id = forms.IntegerField(widget=forms.HiddenInput())


    class Meta:
        model = User
        fields = (
            'username', 
            'in_game_id',
            'email', 
            'password1', 
            'password2', 
            )
