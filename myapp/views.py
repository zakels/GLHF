# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from myapp.models import Book
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

