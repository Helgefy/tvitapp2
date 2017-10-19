# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Tweet


# Create your views here.
def tweet_list(request):
	queryset_list = Tweet.objects.all()#GET alle tweetene i databasen
	#Paginator kode
	paginator = Paginator(queryset_list, 10) # Show 10 contacts per page
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	
	context = {
		'object_list': queryset,
		'title': 'List',
		'page_request_var':page_request_var,
	}
	return render(request,'tweet_list.html',context)