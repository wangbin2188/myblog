from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^shop_cart/$', views.shop_cart, name='shop_cart'),
	url(r'^mall_index/$',views.mall_index,name='mall_index'),
	url(r'^order_list/$',views.order_list,name='order_list'),
	url(r'^product_detail/(?P<product_id>[0-9]+)/$', views.product_detail, name='product_detail'),
	url(r'^order_detail/(?P<order_id>[0-9]+)/$', views.order_detail, name='order_detail'),
	url(r'^shop_cart_add/(?P<product_id>[0-9]+)/$', views.shop_cart_add, name='shop_cart_add'),
	url(r'^shop_cart_remove/(?P<pi_id>[0-9]+)/$',views.shop_cart_remove,name='shop_cart_remove'),
	url(r'^pay_detail/$',views.pay_detail,name='pay_detail'),
	url(r'^shop_quantity_plus/(?P<product_id>[0-9]+)/$', views.shop_quantity_plus, name='shop_quantity_plus'),
	url(r'^shop_quantity_minus/(?P<product_id>[0-9]+)/$', views.shop_quantity_minus, name='shop_quantity_minus'),
	url(r'^submit_order/(.*?)/$',views.submit_order,name='submit_order'),
	url(r'^submit_success/$',views.submit_success,name='submit_success'),

]
