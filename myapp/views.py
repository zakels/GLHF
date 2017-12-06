# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

import requests, json

from myapp.forms import SignUpForm

api_form = "?api_key="
api_key = api_form + "RGAPI-f096fe9a-d356-42b3-a298-dcab88ddc54e"

# Create your views here.
def index(request):
	if request.user.is_authenticated():
		sid = str(request.user.profile.summoner_id)
		championId = findChampionMasteries(sid)
		championName = findChampionName(championId)
		img_splash = findChampionSplash(championId)

		return render(request, 'index.html', {
				'championId' : championId,
				'championName' : championName,
				'championSplash' : img_splash
			})
	else:
		return render(request, 'index.html')

def findChampionMasteries(sid):
	url = "https://na1.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/" + sid + api_key
	r = requests.get(url)
	data = r.json()
	res = data[0]['championId']
	return res

def findChampionName(cid):
	scid = str(cid)
	json_data = open('myapp/static/db/staticData.json')
	d = json.load(json_data)
	for i in d['data']:
		for j in d['data'][i]:
			if d['data'][i]['id'] == cid:
				res = d['data'][i]['name']
	
	return res

def findChampionKey(cid):
	scid = str(cid)
	json_data = open('myapp/static/db/staticData.json')
	d = json.load(json_data)
	for i in d['data']:
		for j in d['data'][i]:
			if d['data'][i]['id'] == cid:
				res = d['data'][i]['key']
	
	return res

def findChampionSplash(cid):
	key = findChampionKey(cid)
	url = "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/" + key + "_0.jpg"

	return url

def signup(request): 
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            url = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + form.cleaned_data.get('in_game_id') + api_key
            r = requests.get(url)
            data = r.json()
            account_id = '0'
            summoner_id = '0'
            try:
                account_id = json.dumps(data['accountId'])
                summoner_id = json.dumps(data['id'])
            except KeyError:
                form.in_game_id = "";
                return render(request, 'signup.html', {'form': form})
            if(account_id == '0' or summoner_id == '0'):
                form.in_game_id = "";
                return render(request, 'signup.html', {'form': form})
            user = form.save()
            user.refresh_from_db()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user.profile.in_game_id = form.cleaned_data.get('in_game_id')
            user.profile.account_id = account_id
            user.profile.summoner_id = summoner_id
            user.save()
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

