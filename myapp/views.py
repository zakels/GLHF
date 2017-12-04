# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from myapp.models import Book

import requests, json
api_format = "?api_key="
api_key = api_format+"RGAPI-cc796626-90e8-4f70-ac34-f9e41e7a40ca"
# Create your views here.

def DisplayMyPage(request):
    return render(request, 'myapp/mypage.html', { 'welcome_text': 'Hello World!'})

def DisplayMyPageWithParameter(request, my_parameter):
    welcomeText = my_parameter
    return render(request, 'myapp/mypage.html', { 'welcome_text': welcomeText })

def InsertBook(request, isbn, title, memo):
    Book(isbn=isbn, title=title, memo={'content': memo}).save()
    return render(request, 'myapp/mypage.html', { 'welcome_text': 'Insert: ' + title })

def DisplayBook(request, isbn):
    result = Book.objects.filter(isbn=isbn)[0]
    bookInfo = "ISBN: {0}; TITLE: {1};MEMO:{2}".format(result.isbn,result.title,result.memo['content'])
    return render(request, 'myapp/mypage.html', { 'welcome_text': bookInfo})


def findSummonerId(request, summonerName):
 #   api_key = "?api_key=RGAPI-5511d848-5f31-4011-9dcc-a3d2e027ee3b"
    url = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/"+summonerName+api_key
    r = requests.get(url)
    data = r.json()
    return render(request, 'myapp/mypage.html', { 'welcome_text': 'API DATAS: ' + json.dumps(data) })

def convertNameToAccountId(request,summonerName):
    url = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/"+summonerName+api_key
    r = requests.get(url)
    data = r.json()
    return render(request, 'myapp/mypage.html', { 'welcome_text': 'accountId: ' +
        json.dumps(data['accountId']) })

#def convertNameToSummonerId(request, summonerName):
def convertNameToSummonerId(summonerName):
    url = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/"+summonerName+api_key
    r = requests.get(url)
    data = r.json()
    return data['id']
#    return render(request, 'myapp/mypage.html', { 'welcome_text': 'summonerId: ' + json.dumps(data['id']) })

def getSummonerInfo(request, summonerName):
    url =  "https://na1.api.riotgames.com/lol/league/v3/leagues/by-summoner/"+str(convertNameToSummonerId(summonerName))+api_key
    print (url)
    r = requests.get(url)
    data = r.json()
    return render(request, 'myapp/mypage.html', { 'welcome_text': 'SummonerInfo: ' +
        json.dumps(data) })
