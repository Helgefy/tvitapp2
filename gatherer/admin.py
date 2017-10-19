# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Tweet

# Register your models here.

class TweetAdmin(admin.ModelAdmin):
	list_display = ['tweet_id','text','publish_date']
	list_display_links = ['tweet_id']
	list_filter = ['publish_date']
	search_fields = ['text']
	class Meta:
		model = Tweet

admin.site.register(Tweet, TweetAdmin)