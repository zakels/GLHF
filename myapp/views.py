# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

import requests, json

from myapp.forms import SignUpForm

api_form = "?api_key="
api_key = api_form + "RGAPI-cc796626-90e8-4f70-ac34-f9e41e7a40ca"

# Create your views here.
def index(request):
	return render(request, 'index.html')


def signup(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.in_game_id = form.cleaned_data.get('in_game_id')
            url = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + user.profile.in_game_id + api_key
            r = requests.get(url)
            data = r.json()
            user.profile.account_id = json.dumps(data['accountId'])
            user.profile.summoner_id = json.dumps(data['id'])

            user.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def profile(request):
    args = {'user' : request.user}
    return render(request, 'profile.html', args)


# 1
# content_type="application/json"
# json.dumps(user.as_json())

# 2
# from django.core import serializers
# variable_name = serializer.serialize('json', User.objects.all())

