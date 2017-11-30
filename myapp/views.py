# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def DisplayMyPage(request):
    return render(request, 'myapp/mypage.html', { 'welcome_text': 'Hello World!'})

def DisplayMyPageWithParameter(request, my_parameter):
    welcomeText = my_parameter
    return render(request, 'myapp/mypage.html', { 'welcome_text': welcomeText })
