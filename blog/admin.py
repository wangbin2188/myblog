# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db import models
from django import forms
from .models import Comment, Article, Column,Author

class CommentAdmin(admin.ModelAdmin):
	list_display = ('user_id','article_id','pub_date', 'content','poll_num')  

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title','pub_date', 'poll_num') 


class ColumnAdmin(admin.ModelAdmin):
	list_display = ('name', 'intro') 

class AuthorAdmin(admin.ModelAdmin):
	list_display = ('name', 'profile') 

admin.site.register(Comment, CommentAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Author, AuthorAdmin)
