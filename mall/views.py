# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django import forms
from mall.models import Category,Product,ProductItem,RegisterUser,Orders,ShoppingCart,ProductComment
import json
from datetime import datetime,date,timedelta
import urlparse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



# Create your views here.

class ShoppingCartForm(forms.Form):
	products=forms.ModelMultipleChoiceField(queryset=None,widget=forms.CheckboxSelectMultiple())

class OrdersForm(forms.ModelForm):
	class Meta: 
		model = Orders 
		fields = ('receiver','receiver_phone','receiver_address',)
# def index(request):
	# if request.method=='GET':
		# form=ShoppingCartForm()
		# form.fields['products'].queryset = ShoppingCart.objects.get(username=request.user).products.all()
		
		# return render(request,'index.html',{'form':form})

def cart_num(request):
	try:
		sc=ShoppingCart.objects.get(username=request.user)
	except ShoppingCart.DoesNotExist:
		goods=0
		return goods
	goods=sc.products.count()
	return goods

def cart_list(request):
	try:
		sc=ShoppingCart.objects.get(username=request.user)
	except ShoppingCart.DoesNotExist:
		product_list=None
		return product_list
	product_list=sc.products.all()
	return product_list
	
def shop_cart(request):
	goods=cart_num(request)
	if request.method=='GET':
		product_list=cart_list(request)
		return render(request,'shop_cart.html',locals())
	elif request.method=='POST':
		product_list=cart_list(request)
		pi_ids=request.POST.getlist('products')
		pi_quantity=[]
		pi_price=[]
		for pid in pi_ids:
			pi_quantity.append(ProductItem.objects.get(id=pid).quantity)
			pi_price.append(ProductItem.objects.get(id=pid).product_name.product_price)
		pay_price=sum([a*b for a, b in zip(pi_quantity,pi_price)])
		#return redirect('submit_order',pi_ids=','.join(pi_ids))
		url = urlparse.urljoin('/mall/submit_order/','%s/'%(",".join(pi_ids)))
		return redirect(url)
def shop_cart_remove(request,pi_id):
	if request.method=='GET':
		pi=ProductItem.objects.get(id=pi_id)
		sc=ShoppingCart.objects.get(username=request.user)
		sc.products.remove(pi)
		sc.save()
		pi.delete()
		return redirect('shop_cart')

def submit_order(request,pi_ids):

	id_list=[int(x) for x in pi_ids.split(',')]
	product_items=ProductItem.objects.filter(id__in=id_list)
	pi_quantity=[]
	pi_price=[]
	for pid in id_list:
		pi_quantity.append(ProductItem.objects.get(id=pid).quantity)
		pi_price.append(ProductItem.objects.get(id=pid).product_name.product_price)
	amount=sum([a*b for a, b in zip(pi_quantity,pi_price)])

		
	if request.method=='GET':
		current_user=RegisterUser.objects.get(username=request.user)
		form=OrdersForm(initial={'receiver':current_user.username.first_name,
					'receiver_phone':current_user.user_phone,
					'receiver_address':current_user.user_address})
		return render(request,'submit_order.html',locals())
	elif request.method=='POST':
		form=OrdersForm(request.POST)
		if form.is_valid():
			receiver=form.cleaned_data['receiver']
			receiver_phone=form.cleaned_data['receiver_phone']
			receiver_address=form.cleaned_data['receiver_address']
			obj=Orders(consumer=request.user,receiver=receiver,receiver_phone=receiver_phone,receiver_address=receiver_address,amount=amount,order_status=1)
			obj.save()
			obj.products=product_items
			obj.save()
			# 商品条目不能删除，但是需要从购物车里删掉
			sc=ShoppingCart.objects.get(username=request.user)
			for pi in product_items:
				if pi in sc.products.all():
					sc.products.remove(pi)
			sc.save()
			return redirect('order_list')
		
def submit_success(request):
	return HttpResponse(u"订单创建成功!")
		
def mall_index(request):
	goods=cart_num(request)
	if request.method=='GET':
		product_list=Product.objects.all()
		return render(request,'mall_index.html',locals())
	elif request.method=='POST':
		search_content=request.POST.get('search')
		product_list=Product.objects.filter(product_name__icontains=search_content)
		return render(request,'mall_index.html',locals())

def product_detail(request,product_id):
	goods=cart_num(request)
	if request.method=='GET':
		product_detail=Product.objects.get(id=product_id)
		# 用户立即购买时会创建一个无用户的商品条目对象,如果本来就有一定不会新加
		obj, created=ProductItem.objects.update_or_create(product_name=product_detail,quantity=1,username=None)
		product_items=ProductItem.objects.get(product_name=product_detail,username=None)
		return render(request,'product_detail.html',locals())
		
def order_list(request):
	goods=cart_num(request)
	if request.method=='GET':
		order_list=Orders.objects.filter(consumer=request.user)
		return render(request,'order_list.html',locals())

def order_detail(request,order_id):
	goods=cart_num(request)
	if request.method=='GET':
		order_detail=Orders.objects.get(id=order_id)
		return render(request,'order_detail.html',locals())
		
def shop_cart_add(request,product_id):
	goods=cart_num(request)
	if request.method=='GET':
		# 如果有购物车就获取购物车对象，没有购物车，那么先创建一个
		# 创建购物车之前先给用户创建产品条目
		product_item,created=ProductItem.objects.get_or_create(product_name=Product.objects.get(id=product_id),quantity=1,username=request.user)
		obj,created2=ShoppingCart.objects.get_or_create(username=request.user)
		# 将产品条目加入购物车之前需要有一个判断，购物车是否是空车？购物车里是否有同类产品
		current_cart=obj.products.all()
		for old_pi in current_cart:
			if old_pi.product_name == product_item.product_name:
				product_item.quantity=product_item.quantity + old_pi.quantity
				product_item.save()
				obj.products.remove(old_pi)
				if created:
					old_pi.delete()
				obj.products.add(product_item)
				return redirect('product_detail',product_id=product_id)

		obj.products.add(product_item)
		obj.save()

		return redirect('product_detail',product_id=product_id)
		
def pay_detail(request):
	pass 
	
def shop_quantity_plus(request,product_id):
	goods=cart_num(request)
	if request.method=='GET':
		obj=ShoppingCart.objects.get(username=request.user)
		current_cart=obj.products.all()
		p=Product.objects.get(id=product_id)
		pi=ProductItem.objects.get(product_name=p,username=request.user)
		obj.products.remove(pi)
		pi.quantity=pi.quantity+1
		pi.save()
		obj.products.add(pi)
		return redirect('shop_cart')
		
def shop_quantity_minus(request,product_id):
	goods=cart_num(request)
	if request.method=='GET':
		obj=ShoppingCart.objects.get(username=request.user)
		current_cart=obj.products.all()
		p=Product.objects.get(id=product_id)
		pi=ProductItem.objects.get(product_name=p,username=request.user)	
		if pi.quantity<=1:
			return redirect('shop_cart')
		else:
			obj.products.remove(pi)
			pi.quantity=pi.quantity-1
			pi.save()
			obj.products.add(pi)
			return redirect('shop_cart')

		

	
	
