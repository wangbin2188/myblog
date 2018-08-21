# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment, Poll,Column
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

import markdown2, urlparse
def column(request,column_id):
	column_list = Column.objects.all
	logged_user = request.user
	collect_list = logged_user.article_set.all()
	column_article_list = Article.objects.query_by_column(column_id)
	context = {'column_article_list': column_article_list,'column_list':column_list,'collect_list':collect_list}
	return render(request, 'column.htm', context)
	
def article(request, article_id):
	'''
	try:   # since visitor input a url with invalid id
		article = Article.objects.get(pk=article_id)  # pk??? 
	except Article.DoesNotExist:
		raise Http404("Article does not exist")
	''' # shortcut:
	column_list = Column.objects.all
	logged_user = request.user
	collect_list = logged_user.article_set.all()
	poll_list= logged_user.poll_set.all()
	article = get_object_or_404(Article, id=article_id)
	content = markdown2.markdown(article.content, extras=["code-friendly","fenced-code-blocks", "header-ids", "toc", "metadata"])
	commentform = CommentForm()
	comments = article.comment_set.all
	related_list=Article.objects.query_by_column(article.column_id).exclude(id=article_id)
	return render(request, 'article_page.htm', {
		'article': article, 
		'commentform':commentform,
		'content': content,
		'comments': comments,
		'collect_list':collect_list,
		'column_list':column_list,
		'poll_list':poll_list,
		'related_list':related_list
		})

@login_required  
def comment(request, article_id):
	form  = CommentForm(request.POST)
	url = urlparse.urljoin('/blog/', article_id)
	if form.is_valid():
		user = request.user
		article = Article.objects.get(id=article_id)
		new_comment = form.cleaned_data['comment']
		c = Comment(content=new_comment, article_id=article_id)  # have tested by shell
		c.user = user
		c.save()
		article.comment_num += 1
		article.save()
	return redirect(url)

@login_required
def get_keep(request, article_id):
	logged_user = request.user
	article = Article.objects.get(id=article_id) 
	articles = logged_user.article_set.all()
	url = urlparse.urljoin('/blog/', article_id)
	if article not in articles:	
		article.user.add(logged_user)  # for m2m linking, have tested by shell
		article.keep_num += 1
		article.save()
		return redirect(url)
	else:
		return redirect(url)

@login_required
def get_poll_article(request,article_id):
	logged_user = request.user
	article = Article.objects.get(id=article_id)
	polls = logged_user.poll_set.all()
	url = urlparse.urljoin('/blog/', article_id)
	articles = []
	for poll in polls:
		articles.append(poll.article)

	if article in articles:
		return redirect(url)
	else:
		article.poll_num += 1
		article.save()
		poll = Poll(user=logged_user, article=article)
		poll.save()
		data = {}   
		return redirect(url)



