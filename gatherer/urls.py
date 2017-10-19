from django.conf.urls import url
from django.contrib import admin

from .views import(
	tweet_list,
	)

urlpatterns = [
    url(r'^$', tweet_list,name='list'),
]