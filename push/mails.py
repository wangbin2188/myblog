# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from push.models import AppIndex,AppDaily,LogList
from django.core import serializers
from django.contrib.auth.models import User
from push.forms import DailyStartForm
from django.shortcuts import render,render_to_response,redirect
import urlparse
import json
from datetime import datetime,timedelta
from django.template import Context, loader 
import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 
from_email = settings.DEFAULT_FROM_EMAIL

now=datetime.now()
last_day =now-timedelta(days=1)
dt=last_day.strftime('%Y-%m-%d')

def email_test(request):
	send_mail('Subject here', 'Here is the message.', from_email,['wangbin10@yiche.com'], fail_silently=False)
	return HttpResponse('email_test') 

def log_export(request,ids):
	email_template_name = 'loglist_tem.htm'
	data_dict={}
	id_list=[int(x) for x in ids.split(',')]
	loglist=LogList.objects.filter(id__in=id_list)
	t = loader.get_template(email_template_name)
	to_email=['lijiang@yiche.com','huangg@yiche.com','wangbin10@yiche.com',request.user.email]
	email_title='日志埋点'
	data_dict['loglist']=loglist
	html_content = t.render(Context(data_dict))
	msg = EmailMultiAlternatives(email_title,html_content,from_email,to_email)
	msg.attach_alternative(html_content, "text/html")
	msg.content_subtype = "html"
	msg.send()
	return render(request,email_template_name,data_dict)
	
@login_required(login_url='/push/push_login/')
def daily_start(request):
	if request.POST:
		form=DailyStartForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			daily_name=form.cleaned_data['daily_name']
			url = urlparse.urljoin('/push/','%s/%s/'%(daily_name,start_date))
			return redirect(url)
			
	else:
		form=DailyStartForm()
		return render(request,"daily_start.htm",{'form':form})
		
@permission_required('push.add_user', login_url='/push/push_login/')
def car_daily(request,dt=dt):
	email_template_name = 'car_daily_tem.htm'
	data_dict={}
	t = loader.get_template(email_template_name)
	email_data=User.objects.filter(appdaily__daily_key='car_daily').values('email')
	to_email=[item['email'] for item in list(email_data)]
	daily_data=AppDaily.objects.filter(daily_key='car_daily').values('daily_desc')
	email_title=list(daily_data)[0]['daily_desc']

	# appindex
	appstay = serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='appstay').order_by('dt'))
	appstay=list(map(lambda x:x['fields'],json.loads(appstay)))
	data_dict['car_stay']=json.loads(appstay[0]['c_value'])['TabXuanChe']
	
	car_evaluation = serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='car_evaluation').order_by('dt'))
	car_evaluation=list(map(lambda x:x['fields'],json.loads(car_evaluation)))
	data_dict['car_evaluation_add']    =json.loads(car_evaluation[0]['c_value'])['evaluation_add']
	data_dict['car_evaluation_comment']=json.loads(car_evaluation[0]['c_value'])['evaluation_comment']
	data_dict['pc_evaluation_add']    =json.loads(car_evaluation[0]['c_value'])['pc_evaluation_add']
	data_dict['pc_evaluation_comment']=json.loads(car_evaluation[0]['c_value'])['pc_evaluation_comment']
	
	photos = serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='photos').order_by('dt'))
	photos=list(map(lambda x:x['fields'],json.loads(photos)))
	data_dict['car_photo_uv']=json.loads(photos[0]['c_value'])['car_photo_uv']
	data_dict['car_photo_pv']=json.loads(photos[0]['c_value'])['car_photo_pv']
	
	business=serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='log_business').order_by('dt'))
	business=list(map(lambda x:x['fields'],json.loads(business)))
	business_dict=json.loads(business[0]['c_value'])
	data_dict=dict(data_dict,**business_dict)

	module=serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='log_module').order_by('dt'))
	module=list(map(lambda x:x['fields'],json.loads(module)))
	module_dict=json.loads(module[0]['c_value'])
	data_dict=dict(data_dict,**module_dict)
	
	car_summary=serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='car_summary').order_by('dt'))
	car_summary=list(map(lambda x:x['fields'],json.loads(car_summary)))
	car_summary_dict=json.loads(car_summary[0]['c_value'])
	data_dict=dict(data_dict,**car_summary_dict)
	
	car_icon=serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='car_icon').order_by('dt'))
	car_icon=list(map(lambda x:x['fields'],json.loads(car_icon)))
	car_icon_dict=json.loads(car_icon[0]['c_value'])
	data_dict=dict(data_dict,**car_icon_dict)	
	
	car_func=serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='car_func').order_by('dt'))
	car_func=list(map(lambda x:x['fields'],json.loads(car_func)))
	car_func_dict=json.loads(car_func[0]['c_value'])
	data_dict=dict(data_dict,**car_func_dict)	

	subkey=['car_summary_pv','car_params_pv','car_discount_pv','car_evaluation_pv','car_news_pv','car_video_pv','car_sale_pv','car_community_pv']
	subdict=dict([(key,int(data_dict[key])) for key in subkey])
	car_sum=sum(subdict.values())
	data_dict['car_sum']=car_sum
	data_dict['dt']=dt
	html_content = t.render(Context(data_dict))
	msg = EmailMultiAlternatives(email_title,html_content,from_email,to_email)
	msg.attach_alternative(html_content, "text/html")
	msg.content_subtype = "html"
	msg.send()
	return render(request,email_template_name,data_dict)

@permission_required('push.add_user', login_url='/push/push_login/')
def headline_daily(request,dt=dt):
	email_template_name = 'headline_daily_tem.htm'
	data_dict={}
	t = loader.get_template(email_template_name)
	email_data=User.objects.filter(appdaily__daily_key='headline_daily').values('email')
	to_email=[item['email'] for item in list(email_data)]
	daily_data=AppDaily.objects.filter(daily_key='headline_daily').values('daily_desc')
	email_title=list(daily_data)[0]['daily_desc']
	
	appstay = serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='appstay').order_by('dt'))
	appstay=list(map(lambda x:x['fields'],json.loads(appstay)))
	data_dict['headline_stay']=json.loads(appstay[0]['c_value'])['TabTouTiao']
	
	module=serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='log_module').order_by('dt'))
	module=list(map(lambda x:x['fields'],json.loads(module)))
	module_dict=json.loads(module[0]['c_value'])
	data_dict=dict(data_dict,**module_dict)

	headline_pv=serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='headline_pv').order_by('dt'))
	headline_pv=list(map(lambda x:x['fields'],json.loads(headline_pv)))
	headline_pv=json.loads(headline_pv[0]['c_value'])
	data_dict=dict(data_dict,**headline_pv)

	headline_uv=serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='headline_uv').order_by('dt'))
	headline_uv=list(map(lambda x:x['fields'],json.loads(headline_uv)))
	headline_uv=json.loads(headline_uv[0]['c_value'])
	data_dict=dict(data_dict,**headline_uv)


	media=serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='media').order_by('dt'))
	media=list(map(lambda x:x['fields'],json.loads(media)))
	media=json.loads(media[0]['c_value'])
	data_dict=dict(data_dict,**media)

	news=serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='news_add&com').order_by('dt'))
	news=list(map(lambda x:x['fields'],json.loads(news)))
	news=json.loads(news[0]['c_value'])
	data_dict=dict(data_dict,**news)

	live=serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='live_add&com').order_by('dt'))
	live=list(map(lambda x:x['fields'],json.loads(live)))
	live=json.loads(live[0]['c_value'])
	data_dict=dict(data_dict,**live)
	
	album=serializers.serialize("json", AppIndex.objects.filter(dt=dt,c_key='album&video').order_by('dt'))
	album=list(map(lambda x:x['fields'],json.loads(album)))
	album=json.loads(album[0]['c_value'])	
	data_dict=dict(data_dict,**album)
	
	data_dict['dt']=dt
	html_content = t.render(Context(data_dict))
	msg = EmailMultiAlternatives(email_title,html_content,from_email,to_email)
	msg.attach_alternative(html_content, "text/html")
	msg.content_subtype = "html"
	msg.send()
	return render(request,email_template_name,data_dict)
