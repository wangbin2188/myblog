from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^flow_create/$', views.flow_create, name='flow_create'),
	url(r'^flow_approval/(?P<flow_id>[0-9]+)/$', views.flow_approval, name='flow_approval'),
	url(r'^flow_stop/(?P<flow_id>[0-9]+)/$', views.flow_stop, name='flow_stop'),
	url(r'^demand_wake/(?P<flow_id>[0-9]+)/$', views.demand_wake, name='demand_wake'),
    url(r'^flow_submit/$', views.flow_submit, name='flow_submit'),
    url(r'^flow_processed/$', views.flow_processed, name='flow_processed'),
	url(r'^flow_waitfor/$', views.flow_waitfor, name='flow_waitfor'),
	url(r'^flow_complete/$', views.flow_complete, name='flow_complete'),
	url(r'^demand_create/$', views.demand_create, name='demand_create'),
	url(r'^demand_approval/(?P<flow_id>[0-9]+)/$', views.demand_approval, name='demand_approval'),
	url(r'^flow_add/$',views.flow_add,name='flow_add'),
	url(r'^demand_chart/$',views.demand_chart,name='demand_chart'),
	url(r'^demand_update/(?P<flow_id>[0-9]+)/$', views.demand_update, name='demand_update'),
	url(r'^demand_distribute/(?P<flow_id>[0-9]+)/$', views.demand_distribute, name='demand_distribute'),
]
