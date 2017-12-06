# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

import requests, json, datetime

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
		playerStat = findPlayerStat(sid)
		tier = playerStat['tier']
		rank = playerStat['rank']
		wins = playerStat['wins']
		losses = playerStat['losses']
		return render(request, 'index.html', {
				'championName' : championName,
				'championSplash' : img_splash,
				'tier' : tier,
				'rank' : rank,
				'wins' : wins,
				'losses' : losses
			})
	else:
		return render(request, 'index.html')

def recent(request, user=None):
        if user == None:
            aid = str(request.user.profile.account_id)
            user = str(request.user.profile.in_game_id)
        else:
            aid = str(findIds(user)['aid'])
            user = str(user)
	match_info = getRecentMatches(aid)

	game_id_1 = match_info[0]['gameId']
	lane_1 = match_info[0]['lane']
	champion_1 = findChampionName(match_info[0]['champion'])
	timestamp_1 = datetime.datetime.fromtimestamp(match_info[0]['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

        game_id_2 = match_info[1]['gameId']
        lane_2 = match_info[1]['lane']
	champion_2 = findChampionName(match_info[1]['champion'])
	timestamp_2 = datetime.datetime.fromtimestamp(match_info[1]['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

	game_id_3 = match_info[2]['gameId']
	lane_3 = match_info[2]['lane']
	champion_3 = findChampionName(match_info[2]['champion'])
	timestamp_3 = datetime.datetime.fromtimestamp(match_info[2]['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

        game_id_4 = match_info[3]['gameId']
	lane_4 = match_info[3]['lane']
	champion_4 = findChampionName(match_info[3]['champion'])
	timestamp_4 = datetime.datetime.fromtimestamp(match_info[3]['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

	game_id_5 = match_info[4]['gameId']
	lane_5 = match_info[4]['lane']
	champion_5 = findChampionName(match_info[4]['champion'])
	timestamp_5 = datetime.datetime.fromtimestamp(match_info[4]['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

	return render(request, 'recent.html', {
                        'summonerName' : user,
			'game_id_1' : game_id_1,
			'lane_1' : lane_1,
			'champion_1' : champion_1,
			'timestamp_1' : timestamp_1,
			'game_id_2' : game_id_2,
			'lane_2' : lane_2,
			'champion_2' : champion_2,
			'timestamp_2' : timestamp_2,
			'game_id_3' : game_id_3,
			'lane_3' : lane_3,
			'champion_3' : champion_3,
			'timestamp_3' : timestamp_3,
			'game_id_4' : game_id_4,
			'lane_4' : lane_4,
			'champion_4' : champion_4,
			'timestamp_4' : timestamp_4,
			'game_id_5' : game_id_5,
			'lane_5' : lane_5,
			'champion_5' : champion_5,
			'timestamp_5' : timestamp_5,
		})

def getRecentMatches(aid):
	r_matches = dict()
	url = "https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/" + aid +  api_key + "&beginIndex=0&endIndex=5"
	r = requests.get(url)
	data = r.json()
	res = data['matches']

	return res


# def search(request):
# 	query = request.GET['q']
# 	ids = findIds(query)
# 	sid = ids['sid']
# 	championId = findChampionMasteries(sid)
# 	championName = findChampionName(championId)

# #	t = loader.get_template('search.html')
# #	c = Context({ 'query' : query, })

# 	return render(request, 'search.html', {
# 			'championName' : championName,
# 		})

def findChampionMasteries(sid):
	url = "https://na1.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/" + sid + api_key
        r = requests.get(url)
	data = r.json()
        res = 'No DATA'
        if(len(data) > 0):
            res = data[0]['championId']
	return res

def findChampionName(cid):
	json_data = open('myapp/static/db/staticData.json')
	d = json.load(json_data)
        res = 'No DATA'
	for i in d['data']:
		for j in d['data'][i]:
			if d['data'][i]['id'] == cid:
				res = d['data'][i]['name']
	return res

def findChampionKey(cid):
	json_data = open('myapp/static/db/staticData.json')
	d = json.load(json_data)
        res = 'No DATA'
	for i in d['data']:
		for j in d['data'][i]:
			if d['data'][i]['id'] == cid:
				res = d['data'][i]['key']
	return res

def findChampionSplash(cid):
	key = findChampionKey(cid)
	url = "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/" + key + "_0.jpg"
	return url

def findPlayerStat(sid):
	d_playerstat = dict()
	url = "https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/" + sid + api_key
	r = requests.get(url)
	data = r.json()

	tier = 'UNRANKED'
	rank = 'X'
	wins = 0
	losses = 0

	for item in data:
		if "RANKED_SOLO_5x5" in item['queueType']:
			tier = item['tier']
			rank = item['rank']
			wins = item['wins']
			losses = item['losses']

	d_playerstat['tier'] = tier
	d_playerstat['rank'] = rank
	d_playerstat['wins'] = wins
	d_playerstat['losses'] = losses

	return d_playerstat

def findIds(in_game_id):
	d_ids = dict()
	url = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + in_game_id + api_key
	r = requests.get(url)
	data = r.json()
	try:
		account_id = data['accountId']
		summoner_id = data['id']
		d_ids['aid'] = account_id
		d_ids['sid'] = summoner_id
	except KeyError:
		return d_ids

	return d_ids

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
    if request.method == 'POST':
        ids = findIds(request.POST.get('q', ''))
#	if request.user.is_authenticated():
        sid = str(ids['sid'])
        summonerName = request.POST.get('q', '')
        championId = findChampionMasteries(sid)
        championName = findChampionName(championId)
        img_splash = findChampionSplash(championId)
        playerStat = findPlayerStat(sid)
        tier = playerStat['tier']
        rank = playerStat['rank']
        wins = playerStat['wins']
        losses = playerStat['losses']
        return render(request, 'index.html', {
		'championName' : championName,
		'championSplash' : img_splash,
                'summonerName' : summonerName,
		'tier' : tier,
		'rank' : rank,
		'wins' : wins,
		'losses' : losses
	})
    else:
	return render(request, 'index.html')

# 1
# content_type="application/json"
# json.dumps(user.as_json())

# 2
# from django.core import serializers
# variable_name = serializer.serialize('json', User.objects.all())

