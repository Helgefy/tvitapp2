# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Tweet(models.Model):
	tweet_id = models.CharField(max_length=100)
	text = models.CharField(max_length=300)
	publish_date = models.DateField(auto_now=True,auto_now_add=False)
	html = models.TextField()


class myTweet(models.Model):
	tweet_id = models.CharField(max_length=100)
	text = models.CharField(max_length=160)
	publish_date = models.DateField(auto_now=True,auto_now_add=False)
	html = models.TextField() #trenger kanskje ikke denne hvis vi får tweetstreemen til brukeren