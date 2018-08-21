# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Category(models.Model):
	first_c  = models.CharField(verbose_name='一级分类',max_length=20)
	second_c = models.CharField(verbose_name='二级分类',max_length=20)
	three_c  = models.CharField(verbose_name='三级分类',max_length=20)
	
	def __unicode__(self):
		return u'%s-%s-%s' % (self.first_c,self.second_c,self.three_c)

class Product(models.Model):
	brand           = models.CharField(verbose_name='品牌',max_length=20)
	product_name    = models.CharField(verbose_name='商品名称',max_length=40)
	product_price   = models.IntegerField(verbose_name='价格')
	product_desc    = models.TextField(verbose_name='描述')
	create_date     = models.DateField(verbose_name='创建日期',auto_now_add=True)
	update_date     = models.DateField(verbose_name='更新日期',auto_now=True)
	inventory       = models.IntegerField(verbose_name='库存量')
	category        = models.ForeignKey(Category,verbose_name='商品类别')
	related_products=models.ManyToManyField('Product',null=True,blank=True,verbose_name='相关商品')
	
	def __unicode__(self):
		return self.product_name
		
	# def get_absolute_url(self):
		# return reverse('view_name',args=(self.id,))
class ProductItem(models.Model):
	product_name=models.ForeignKey(Product,verbose_name='商品')
	quantity    =models.IntegerField(default=1,verbose_name='商品数量')
	username    = models.ForeignKey(User,verbose_name='用户',null=True,on_delete=models.SET_NULL,related_name='product_user')
	def __unicode__(self):
		return self.product_name.product_name

class RegisterUser(models.Model):
	username     = models.ForeignKey(User,verbose_name='用户姓名',related_name='register_user')
	user_phone   = models.CharField(max_length=11,default='',verbose_name='手机号')
	user_address = models.TextField(verbose_name='地址')
	def __unicode__(self):
		return self.username.first_name

class Orders(models.Model):
	consumer         = models.ForeignKey(User,verbose_name='购买人',related_name='consumer_user')
	create_time      = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
	update_time      = models.DateTimeField(verbose_name='更新时间',auto_now=True)
	receiver         = models.CharField(verbose_name='收货人',max_length=20)
	receiver_phone   = models.CharField(max_length=11,default='',verbose_name='收货手机号')
	receiver_address = models.TextField(verbose_name='收货地址')
	amount           = models.IntegerField(verbose_name='订单总价')
	products         = models.ManyToManyField(ProductItem,verbose_name='商品')
	order_status     = models.IntegerField(verbose_name='订单状态')
	logistics        = models.IntegerField(verbose_name='运单号',null=True)
	
	# def get_absolute_url(self):
		# return reverse('view_name',args=(self.id,))

class ShoppingCart(models.Model):
	username    = models.ForeignKey(User,verbose_name='用户名',related_name='cart_user')
	products    = models.ManyToManyField(ProductItem,verbose_name='商品',null=True)
	create_date = models.DateField(verbose_name='创建日期',auto_now_add=True)
	update_date = models.DateField(verbose_name='更新日期',auto_now=True)
	
	# def get_absolute_url(self):
		# return reverse('view_name',args=(self.id,))

class ProductComment(models.Model):
	consumer    = models.ForeignKey(User,verbose_name='购买人',related_name='comment_user')
	product     = models.ForeignKey(Product,verbose_name='商品名')
	comment     = models.TextField(verbose_name='评价内容')
	create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
	score       = models.IntegerField(verbose_name='评分')
	
	def __unicode__(self):
		return self.comment
	
