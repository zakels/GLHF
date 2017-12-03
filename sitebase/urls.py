"""sitebase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from myapp import views as MyAppView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mypage/', MyAppView.DisplayMyPage),
    url(r'^mypage_param/(?P<my_parameter>.+)', MyAppView.DisplayMyPageWithParameter),
    url(r'^insert/(?P<isbn>.+);(?P<title>.+);(?P<memo>.*)', MyAppView.InsertBook),
    url(r'^show/(?P<isbn>.+)',MyAppView.DisplayBook),
    url(r'^testfind/(?P<summonerName>.+)',MyAppView.findSummonerId),
]
