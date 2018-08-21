# -*- coding: UTF-8 -*-
from django.shortcuts import render,render_to_response,redirect
from django.contrib.auth.models import User
from django.db.models import Q,F 
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import logout
from django.http import HttpResponse
from push.models import Push,AfterOpen,PushClick,PushActive,AreaActive,LossActive,UserList,AppOperate
from push.models import AppFunnel,AppBusiness,CarConversion
from push.models import Channel,AppKey,AppIndex,AppChart,AppDaily,LogList
from django.db.models import Avg,Sum,Count
from django.core import serializers
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from push.forms import AfterOpenForm,LoginForm,AppActiveForm
from push.forms import PushForm,ModuleUserForm,DataCompareForm,CommunityConverForm
from push.forms import PushSendForm,PostDetailForm,RegisterForm,ForgetPasswordForm,ResetPasswordForm
from push.forms import AppStayForm,NewsDataForm,NewsRealForm,PostsRealForm,ChannelForm,AppIndexForm,AppIndexSingleForm,LogListForm
import json
from collections import OrderedDict
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from datetime import datetime,date,timedelta
import csv 
from math import sqrt
from scipy.stats import ttest_ind
from scipy import stats
from sklearn import datasets, linear_model
import urllib
import urllib2
import logging
from django.core.mail import send_mail
from django.conf import settings
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# Author.objects.values('name').annotate(average_rating=Avg('book__rating'))
# Create your views here.
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from push.models import UserList
from django.core.urlresolvers import reverse_lazy
class UserListList(ListView):
	model=UserList
class UserListDetail(DetailView):
	model=UserList
class UserCreate(CreateView):
	model=UserList
	fields=['username','password']
	success_url = '/push/userlist/'
class UserUpdate(UpdateView):
	model=UserList
	fields=['username','password']
	success_url = '/push/userlist/'
	template_name_suffix = '_update_form'
class UserDelete(DeleteView):
	model=UserList
	success_url = reverse_lazy('userlist')

def str2md5(username,email):
	str=username+email[::-1]
	md5 = hashlib.md5()
	md5.update(str.encode('utf-8'))
	str_md5=md5.hexdigest()
	return str_md5

def push_login(request):
	if request.method =='GET':
		form=LoginForm()
		register_msg='没有账号？立即注册！'
		return render(request,'push_login.htm', {'form': form,'register_msg':register_msg})
	elif request.method=='POST':
		form=LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			try:
				user=User.objects.get(username=username)
			except User.DoesNotExist:
				register_msg='没有账号？立即注册！'
				return render(request,'push_login.htm', {'form': form,'register_msg':register_msg})
			user = authenticate(username=username, password=password)
			if user is None:
				forget_msg='忘记密码'
				return render(request,'push_login.htm', {'form': form,'forget_msg':forget_msg})
			else:
				if user.is_active:
					login(request, user)
					return redirect('/push/app_active/')

		else:
			form=LoginForm()
			msg='账号或密码错误'
			return render(request,'push_login.htm', {'form': form,'msg':msg})


def logout_view(request):
	logout(request)
	form=LoginForm()
	return redirect('/push/push_login/')


def register(request):
	if request.method == 'GET':
		form= RegisterForm()
		return render(request,'register.htm',{'form':form})
	elif request.method == 'POST':
		form= RegisterForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			email=form.cleaned_data['email']
			password=form.cleaned_data['password']
			user = User.objects.create_user(username,email,password)
			user.save()
			return redirect('/push/push_login/')
			
def forget_password(request):
	if request.method =='GET':
		form=ForgetPasswordForm()
		return render(request,'forget_password.htm',{'form':form})
	elif request.method =='POST':
		form=ForgetPasswordForm(request.POST)
		if form.is_valid():	
			username=form.cleaned_data['username']
			email=form.cleaned_data['email']
			init_email=User.objects.filter(username=username).values('email')
			init_email=list(init_email)[0]['email']
			if email !=init_email:
				msg='邮箱和注册邮箱不符，请重新输入！'
				return render(request,'forget_password.htm',{'form':form,'msg':msg})
			emails=[]
			emails.append(form.cleaned_data['email'])
			encrypt=str2md5(username,email)
			url='http://172.20.4.64:8000/push/reset_password/'+encrypt+'/'
			send_mail('重置密码',url,settings.DEFAULT_FROM_EMAIL,emails,fail_silently=False)
			msg='密码重置链接已发至您的邮箱!'
			res=render(request,'forget_password.htm',{'form':form,'msg':msg})
			res.set_cookie("reset_username",username)
			res.set_cookie("reset_email",email)
			return res
		else:
			msg='用户名或邮箱输入错误，请重新输入！'
			return render(request,'forget_password.htm',{'form':form,'msg':msg})
	
def reset_password(request,encrypt):
	if request.method == 'GET':
		form= ResetPasswordForm()
		return render(request,'reset_success.htm',{'form':form})
	elif request.method == 'POST':
		form= ResetPasswordForm(request.POST)
		if form.is_valid():
			new_password=form.cleaned_data['password']
			username=request.COOKIES.get("reset_username")
			email=request.COOKIES.get("reset_email")
			if str2md5(username,email)==encrypt:
				u = User.objects.get(username=username)
				u.set_password(new_password)
				u.save()
				msg='密码重置成功!'
				url='立即登录'
				return render(request,'reset_success.htm',{'form':form,'msg':msg,'url':url})
			else:
				msg='错误的链接!'
				return render(request,'reset_success.htm',{'form':form,'msg':msg})

def loglist_create(request):
	if request.method == 'GET':
		form= LogListForm()
		return render(request,'loglist_create.htm',{'form':form})
	elif request.method == 'POST':
		form= LogListForm(request.POST)
		if form.is_valid():
			version=form.cleaned_data['version']
			type_desc=form.cleaned_data['type_desc']
			type_name=form.cleaned_data['type_name']
			page_name=form.cleaned_data['page_name']
			column_name=form.cleaned_data['column_name']
			section_name=form.cleaned_data['section_name']
			view_name=form.cleaned_data['view_name']
			object_name=form.cleaned_data['object_name']
			object_id=form.cleaned_data['object_id']
			obj=LogList(version=version,
						type_desc=type_desc,
						type_name=type_name,
						page_name=page_name,
						column_name=column_name,
						section_name=section_name,
						view_name=view_name,
						object_name=object_name,
						object_id=object_id)
			obj.save()

logger = logging.getLogger('browse')
def get_newsdetail(page=1):
    url='http://api.ycapp.yiche.com/appnews/TouTiaoV64'
    values={}
    values['page'] = page
    data = urllib.urlencode(values)
    geturl = url + "?"+data
    request = urllib2.Request(geturl)
    response = urllib2.urlopen(request)
    js=json.loads(response.read())
    return js['data']['list']

now=datetime.now()
start_init=now-timedelta(days=7)
end_init  =now-timedelta(days=1)
day_before=end_init-timedelta(days=1)
week_before=end_init-timedelta(days=7)
month_before=end_init-timedelta(days=30)
def day_start(end_init):
	return end_init-timedelta(days=1)

def week_start(end_init):
	num=end_init.weekday()
	return end_init-timedelta(days=num+7)
	
	
def month_start(end_init):
	year=end_init.year
	month=end_init.month
	
	if month==1:
		year=year-1
		month=12
	else:
		month=month-1
	return datetime(year,month,1)
	
def field_label(value):
	return {'new_adr':'adr新增','new_ios':'ios新增','new_app':'app新增','active_adr':'adr活跃','active_ios':'ios活跃','active_app':'app活跃',\
	'video_adr':'adr视频播放','video_ios':'ios视频播放','video_app':'app视频播放','login_adr':'adr登录','login_ios':'ios登录','login_app':'app登录',\
	'headline_user':'头条用户数','community_user':'社区用户数','selectcar_user':'选车用户数','service_user':'服务用户数','headline_read':'头条阅读量','headline_photo':'组图阅读量',\
	'news_add':'新增资讯','news_avg':'平均阅读资讯数','reply_add':'新增评论','like_add':'新增点赞','news_share':'文章分享','sharepage_click':'分享页点击数',\
	'community_posts':'社区发帖数','topic_posts':'主题帖','question_posts':'提问帖','vote_posts':'投票贴','bycar_posts':'提车作业','replies':'回帖数',\
	'likes':'点赞数','interactives':'互动数','attentions':'关注数'}[value]
	

def tran_keys(key_list):
	tp_list=[]
	temp_data=AppKey.objects.all().values('c_key','c_desc')
	you_dict={}
	for item in temp_data:
		you_dict[item['c_key']]=item['c_desc']
	for item in key_list:
		tp_list.append(you_dict[item])
	return tp_list
		
def multipl(a,b):
	sumofab=0.0
	for i in range(len(a)):
		temp=a[i]*b[i]
		sumofab+=temp
	return sumofab
 
def correlation(x,y):
	n=len(x)
	sum1=sum(x)
	sum2=sum(y)
	sumofxy=multipl(x,y)
	sumofx2 = sum([pow(i,2) for i in x])
	sumofy2 = sum([pow(j,2) for j in y])
	num=sumofxy-(float(sum1)*float(sum2)/n)
	den=sqrt((sumofx2-float(sum1**2)/n)*(sumofy2-float(sum2**2)/n))
	return num/den


def core_indicator(object):
	index_dict=serializers.serialize("json", object.objects.filter(date__gte=week_before.strftime('%Y-%m-%d'),date__lte=end_init.strftime('%Y-%m-%d')))
	index_dict=list(map(lambda x:x['fields'],json.loads(index_dict)))
	field_list=[]
	for _ in index_dict[0]:
		if _ not in ['date','week','month']:
			field_list.append(_)
	for item in index_dict:
		if item['date']==end_init.strftime('%Y-%m-%d'):
			last_day_dict={}
			for unit in field_list:
				last_day_dict['last_day_'+unit]=item[unit]

	for item in index_dict:
		if item['date']==day_before.strftime('%Y-%m-%d'):
			day_before_dict={}
			for unit in field_list:
				day_before_dict['day_before_'+unit]='%.2f'%(100*(float(last_day_dict['last_day_'+unit])/item[unit]-1))+'%'

	for item in index_dict:
		if item['date']==week_before.strftime('%Y-%m-%d'):
			week_before_dict={}
			for unit in field_list:
				week_before_dict['week_before_'+unit]='%.2f'%(100*(float(last_day_dict['last_day_'+unit])/item[unit]-1))+'%'


	return {'last_day_dict':last_day_dict,'day_before_dict':day_before_dict,'week_before_dict':week_before_dict}

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

			

	
def derivative(list1,list2):
	new_list=[]
	list2.pop(0)
	list2.append(0)
	for (x,y) in zip(list1,list2):
		new_list.append(y-x)
	new_list.pop()
	return new_list
	
def data_format(key_list,key_list_cn,date_format,Dict,form):
	chart_data={}
	for element in key_list:
		chart_data[element]=[]
	chart_data[date_format]=[]
	for item in Dict:
		for it in chart_data.keys():
			chart_data[it].append(item[it])
	return {'key_list':json.dumps(key_list),'key_list_cn':json.dumps(key_list_cn),'chart_data':json.dumps(chart_data),'form':form,'result':Dict,'date_format':json.dumps(date_format)}


def data_format3(key_list,key_list_cn,date_format,Dict,form):
	chart_data={}
	for element in key_list:
		chart_data[element]=[]
	#load keys
	for item in Dict:
		for it in chart_data.keys():
			chart_data[it].append(int(json.loads(item['c_value']).get(it,0)))
	#load date	
	chart_data['date']=set([])
	for item in Dict:
		chart_data['date'].add(item['dt'])
	chart_data['date']=sorted(list(chart_data['date']))
	#load table 
	new_dict={}
	new_list=[]
	mid_list=map(list,zip(*chart_data.values()))
	for item in mid_list:
		new_dict=OrderedDict(zip(chart_data.keys(),item))
		new_list.append(new_dict)
	return {'key_list':json.dumps(key_list),'key_list_cn':json.dumps(key_list_cn),'chart_data':json.dumps(chart_data),'form':form,'result':new_list,'date_format':json.dumps(date_format)}
def data_format4(data):
	new_data=[]
	for item in data:
		item['c_value']=json.loads(item['c_value'])
		item['c_value']['dt']=item['dt']
		new_data.append(item['c_value'])
	return new_data
	
def app_operate(request):
	if request.method == 'GET':
		basic= serializers.serialize("json", AppOperate.objects.filter(dt__gte=month_before.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='basic').order_by('dt'))
		basic=list(map(lambda x:x['fields'],json.loads(basic)))
		basic_data=data_format4(basic)
		
		newuser_retain= serializers.serialize("json", AppOperate.objects.filter(dt__gte=month_before.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='newuser_retain').order_by('dt'))
		newuser_retain=list(map(lambda x:x['fields'],json.loads(newuser_retain)))
		newuser_retain_data=data_format4(newuser_retain)

		active_retain= serializers.serialize("json", AppOperate.objects.filter(dt__gte=month_before.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='active_retain').order_by('dt'))
		active_retain=list(map(lambda x:x['fields'],json.loads(active_retain)))
		active_retain_data=data_format4(active_retain)	

		active_date_distribute= serializers.serialize("json", AppOperate.objects.filter(dt__gte=month_before.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='active_date_distribute').order_by('dt'))
		active_date_distribute=list(map(lambda x:x['fields'],json.loads(active_date_distribute)))
		active_date_distribute_data=data_format4(active_date_distribute)	

		active_month_distribute= serializers.serialize("json", AppOperate.objects.filter(dt__gte=month_before.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='active_month_distribute').order_by('dt'))
		active_month_distribute=list(map(lambda x:x['fields'],json.loads(active_month_distribute)))
		active_month_distribute_data=data_format4(active_month_distribute)	

		active_active_distribute= serializers.serialize("json", AppOperate.objects.filter(dt__gte=month_before.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='active_active_distribute').order_by('dt'))
		active_active_distribute=list(map(lambda x:x['fields'],json.loads(active_active_distribute)))
		active_active_distribute_data=data_format4(active_active_distribute)

	return render(request,"app_operate.htm",locals())
	
def app_modules(request):
	if request.method == 'GET':
		server_module= serializers.serialize("json", AppOperate.objects.filter(dt__range=(month_before.strftime('%Y-%m-%d'),end_init.strftime('%Y-%m-%d')),c_key='server_module').order_by('dt'))
		server_module=list(map(lambda x:x['fields'],json.loads(server_module)))
		server_module=data_format4(server_module)
		
		server_headline= serializers.serialize("json", AppOperate.objects.filter(dt__range=(month_before.strftime('%Y-%m-%d'),end_init.strftime('%Y-%m-%d')),c_key='server_headline').order_by('dt'))
		server_headline=list(map(lambda x:x['fields'],json.loads(server_headline)))
		server_headline=data_format4(server_headline)

		server_car= serializers.serialize("json", AppOperate.objects.filter(dt__range=(month_before.strftime('%Y-%m-%d'),end_init.strftime('%Y-%m-%d')),c_key='server_car').order_by('dt'))
		server_car=list(map(lambda x:x['fields'],json.loads(server_car)))
		server_car=data_format4(server_car)	

		server_business= serializers.serialize("json", AppOperate.objects.filter(dt__range=(month_before.strftime('%Y-%m-%d'),end_init.strftime('%Y-%m-%d')),c_key='server_business').order_by('dt'))
		server_business=list(map(lambda x:x['fields'],json.loads(server_business)))
		server_business=data_format4(server_business)	
		
		appstay= serializers.serialize("json", AppIndex.objects.filter(dt__range=(month_before.strftime('%Y-%m-%d'),end_init.strftime('%Y-%m-%d')),c_key='appstay').order_by('dt'))
		appstay=list(map(lambda x:x['fields'],json.loads(appstay)))
		appstay=data_format4(appstay)

	return render(request,"app_modules.htm",locals())
	
def news_real(request):
	if request.POST:
		form=NewsRealForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			news_type=form.cleaned_data['news_type']
			time_scale=form.cleaned_data['time_scale']
			newsid=form.cleaned_data['newsid']
			idlist=newsid.split(',')
			return render(request,"news_real2.htm",{'form':form,'start_date':json.dumps(start_date,cls=CJsonEncoder),'end_date':json.dumps(end_date,cls=CJsonEncoder),'news_type':json.dumps(news_type),'time_scale':json.dumps(time_scale),'newsid':json.dumps(newsid),'idlist':json.dumps(idlist)})
	else:
		form=NewsRealForm()
		return render(request,"news_real2.htm",{'form':form})
		
def news_real2(request,news_type,newsid):
	form=NewsRealForm()
	start_date=end_init.strftime('%Y-%m-%d %H:%M:%S')
	end_date=now.strftime('%Y-%m-%d %H:%M:%S')
	news_type=news_type
	time_scale=60
	newsid=newsid
	idlist=newsid.split(',')
	return render(request,"news_real2.htm",{'form':form,'start_date':json.dumps(start_date,cls=CJsonEncoder),'end_date':json.dumps(end_date,cls=CJsonEncoder),'news_type':json.dumps(news_type),'time_scale':json.dumps(time_scale),'newsid':json.dumps(newsid),'idlist':json.dumps(idlist)})

def posts_real(request):
	if request.POST:
		form=PostsRealForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			posts_type=form.cleaned_data['posts_type']
			time_scale=form.cleaned_data['time_scale']
			newsid=form.cleaned_data['newsid']
			idlist=newsid.split(',')
			return render(request,"posts_real2.htm",{'form':form,'start_date':json.dumps(start_date,cls=CJsonEncoder),'end_date':json.dumps(end_date,cls=CJsonEncoder),'posts_type':json.dumps(posts_type),'time_scale':json.dumps(time_scale),'newsid':json.dumps(newsid),'idlist':json.dumps(idlist)})
	else:
		form=PostsRealForm()
		return render(request,"posts_real2.htm",{'form':form})	

def posts_real2(request,posts_type,newsid):
	form=PostsRealForm()
	start_date=end_init.strftime('%Y-%m-%d %H:%M:%S')
	end_date=now.strftime('%Y-%m-%d %H:%M:%S')
	posts_type=posts_type
	time_scale=3600
	newsid=newsid
	idlist=newsid.split(',')
	return render(request,"posts_real2.htm",{'form':form,'start_date':json.dumps(start_date,cls=CJsonEncoder),'end_date':json.dumps(end_date,cls=CJsonEncoder),'posts_type':json.dumps(posts_type),'time_scale':json.dumps(time_scale),'newsid':json.dumps(newsid),'idlist':json.dumps(idlist)})

def news_detail(request):
	result=[]
	for i in range(1,6):
		detail= get_newsdetail(i)
		for item in detail:
			result.append(item)
	return render(request,"news_detail.htm",{'result':result})	

@permission_required('push.app_business', login_url='/push/push_login/')
def app_business(request):
	key_list=['yipai','yixin','huimaiche','yichehui','ershouche']
	key_list_cn=['易湃','易鑫','惠买车','易车惠','二手车']
	if request.POST:
		form=AppActiveForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			date_format=form.cleaned_data['date_format']
			if date_format=='date':
				Dict = serializers.serialize("json", AppBusiness.objects.filter(date__gte=start_date,date__lte=end_date).order_by('date'))
				Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
				data_set=data_format(key_list,key_list_cn,date_format,Dict,form)
			else:
				Dict = AppBusiness.objects.filter(date__gte=start_date,date__lte=end_date).values(date_format).annotate(yipai=Avg('yipai'),yixin=Avg('yixin'),huimaiche=Avg('huimaiche'),yichehui=Avg('yichehui'),ershouche=Avg('ershouche')).order_by(date_format)
				data_set=data_format(key_list,key_list_cn,date_format,Dict,form)
			return render(request,"push_line.htm",data_set)

				
	else:# 当正常访问时
		form = AppActiveForm()
		Dict = serializers.serialize("json", AppBusiness.objects.filter(date__gte=start_init.strftime('%Y-%m-%d'),date__lte=end_init.strftime('%Y-%m-%d')).order_by('date'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		date_format='date'
		data_set=data_format(key_list,key_list_cn,date_format,Dict,form)
	return render(request,"push_line.htm",data_set)


def topic2mode(TopicMode):
	if TopicMode==0:
		return 'topic_posts'
	elif TopicMode==1:
		return 'activity_posts'
	elif TopicMode==2:
		return 'question_posts'
	elif TopicMode==3:
		return 'share_posts'
	elif TopicMode==4:
		return 'vote_posts'
	elif TopicMode==5:
		return 'bycar_posts'
	elif TopicMode==6:
		return 'koubei_posts'	
	elif TopicMode==99:
		return 'all_posts'
	
@permission_required('push.post_detail', login_url='/push/push_login/')	
def post_detail(request):
	key_list=['DailyTopicAdd','AppDailyTopicAdd','AppDailyTopicUv','AppDailyReplyAdd','AppDailyReplyAddUv','DailyLikeCount','DailyHomeCount','AppDailyGoodTopicCount']
	key_list_cn=['发帖数','APP发帖数','APP发帖uv','APP回帖数','APP回帖uv','APP点赞数','首页帖','APP精华帖']
	date_format='date'
	if request.POST:
		form=PostDetailForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			post_format=form.cleaned_data['post_format']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key=topic2mode(int(post_format))).order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
		return render(request,"push_line.htm",data_set)

				
	else:# 当正常访问时
		form = PostDetailForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='all_posts').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,"push_line.htm",data_set)
	
#@login_required(login_url='/push/push_login/')	
@permission_required('push.posts_app', login_url='/push/push_login/')	
def posts_app(request):
	key_list=['topic_posts','question_posts','vote_posts','bycar_posts','share_posts','koubei_posts','activity_posts']
	key_list_cn=['主题帖','提问帖','投票贴','提车作业','头条分享帖','口碑帖','活动帖']
	date_format='date'
	if request.POST:
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='posts_add').order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
		return render(request,"push_line.htm",data_set)

				
	else:# 当正常访问时
		form = PushForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='posts_add').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,"push_line.htm",data_set)

@permission_required('push.car_coin', login_url='/push/push_login/')	
def car_coin(request):
	key_list=['give_pv','give_uv','use_pv','use_uv']
	key_list_cn=['车币发放数','车币发放用户数','车币消耗数','车币消耗用户数']
	date_format='date'
	if request.POST:
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='car_coin').order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
		return render(request,"push_line.htm",data_set)

				
	else:# 当正常访问时
		form = PushForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='car_coin').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,"push_line.htm",data_set)

@permission_required('push.app_media', login_url='/push/push_login/')	
def app_media(request):
	key_list=['AddMediaCount','NewsCount','CommentsCount','VisitCount','ShareCount','SubscribeCount']
	key_list_cn=['新增自媒体账号','新增文章','新增评论','自媒体阅读','自媒体分享','新增自媒体关注']
	date_format='date'
	if request.POST:
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='media').order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
		return render(request,"push_line.htm",data_set)

				
	else:# 当正常访问时
		form = PushForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='media').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,"push_line.htm",data_set)
	

#@login_required(login_url='/push/push_login/')	
@permission_required('push.moduleuser', login_url='/push/push_login/')	
def moduleuser(request):
	key_list=['headline','community','car','service','my']
	key_list_cn=['头条','社区','选车','服务','我的']	
	date_format='date'
	if request.POST:
		form=ModuleUserForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			target_format=form.cleaned_data['target_format']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='module_'+target_format).order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
			return render(request,"push_line.htm",data_set)

				
	else:# 当正常访问时
		form = ModuleUserForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='module_pv').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,"push_line.htm",data_set)

def source_keylist(source):
	return {'news_add&com':['DailyNewsAdd','DailyCommentAdd'],'media':['NewsCount','CommentsCount'],'live_add&com':['live_add','live_comment']}[source]

#@login_required(login_url='/push/push_login/')	
@permission_required('push.news_data', login_url='/push/push_login/')
def news_data(request):
	key_list_cn=['新增资讯','新增评论']
	date_format='date'
	if request.POST:
		form=NewsDataForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			source_format=form.cleaned_data['source_format']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key=source_format).order_by('dt'))
			key_list=source_keylist(source_format)
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
		return render(request,"push_line.htm",data_set)

				
	else:# 当正常访问时
		form = NewsDataForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='news_add&com').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		key_list=['DailyNewsAdd','DailyCommentAdd']
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)	
	return render(request,"push_line.htm",data_set)
	



#@login_required(login_url='/push/push_login/')	
@permission_required('push.app_video', login_url='/push/push_login/')	
def app_video(request):
	key_list=['adr_video','ios_video']
	key_list_cn=['adr视频','ios视频']
	date_format='date'
	if request.POST:
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='server_videoplay').order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)

			return render(request,"push_line.htm",data_set)

				
	else:# 当正常访问时
		form = PushForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='server_videoplay').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,"push_line.htm",data_set)



@permission_required('push.add_carconversion', login_url='/push/push_login/')
def car_conversion(request):
	if request.POST:
		form=AppActiveForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			date_format=form.cleaned_data['date_format']
			if date_format=='date':
				Dict = serializers.serialize("json", CarConversion.objects.filter(date__gte=start_date,date__lte=end_date).order_by('date'))
				Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
				select_date=[]
				car_tab=[]
				car_summary=[]
				car_detail=[]
				agents_detail=[]
				agents_inquiry=[]
				a2b=[]
				b2c=[]
				c2d=[]
				for item in Dict:
					select_date.append(item['date'])
					car_tab.append(item['car_tab'])
					car_summary.append(item['car_summary'])
					car_detail.append(item['car_detail'])
					agents_detail.append(item['agents_detail'])
					agents_inquiry.append(item['agents_inquiry'])
					a2b.append('%.1f'%(100*float(item['car_summary'])/item['car_tab']))
					b2c.append('%.1f'%(100*float(item['car_detail'])/item['car_summary']))
					c2d.append('%.1f'%(100*float(item['agents_detail'])/item['car_detail']))
			else:
				Dict = CarConversion.objects.filter(date__gte=start_date,date__lte=end_date).values(date_format).annotate(car_tab=Avg('car_tab'),car_summary=Avg('car_summary'),car_detail=Avg('car_detail'),agents_detail=Avg('agents_detail'),agents_inquiry=Avg('agents_inquiry')).order_by(date_format)
				select_date=[]
				car_tab=[]
				car_summary=[]
				car_detail=[]
				agents_detail=[]
				agents_inquiry=[]
				a2b=[]
				b2c=[]
				c2d=[]
				for item in Dict:
					select_date.append(item[date_format])
					car_tab.append(item['car_tab'])
					car_summary.append(item['car_summary'])
					car_detail.append(item['car_detail'])
					agents_detail.append(item['agents_detail'])
					agents_inquiry.append(item['agents_inquiry'])
					a2b.append('%.1f'%(100*float(item['car_summary'])/item['car_tab']))
					b2c.append('%.1f'%(100*float(item['car_detail'])/item['car_summary']))
					c2d.append('%.1f'%(100*float(item['agents_detail'])/item['car_detail']))					
					
			return render(request,"car_conversion.htm",{'select_date':json.dumps(select_date),'car_tab':json.dumps(car_tab),'car_summary':json.dumps(car_summary),\
			'car_detail':json.dumps(car_detail),'agents_detail':json.dumps(agents_detail),'agents_inquiry':json.dumps(agents_inquiry),'form':form,'result':Dict,'date_format':date_format,\
			'a2b':json.dumps(a2b),'b2c':json.dumps(b2c),'c2d':json.dumps(c2d)})

				
	else:# 当正常访问时
		form = AppActiveForm()
		Dict = serializers.serialize("json", CarConversion.objects.filter(date__gte=start_init.strftime('%Y-%m-%d'),date__lte=end_init.strftime('%Y-%m-%d')).order_by('date'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		date_format='date'
		select_date=[]
		car_tab=[]
		car_summary=[]
		car_detail=[]
		agents_detail=[]
		agents_inquiry=[]
		a2b=[]
		b2c=[]
		c2d=[]
		for item in Dict:
			select_date.append(item['date'])
			car_tab.append(item['car_tab'])
			car_summary.append(item['car_summary'])
			car_detail.append(item['car_detail'])
			agents_detail.append(item['agents_detail'])
			agents_inquiry.append(item['agents_inquiry'])
			a2b.append('%.1f'%(100*float(item['car_summary'])/item['car_tab']))
			b2c.append('%.1f'%(100*float(item['car_detail'])/item['car_summary']))
			c2d.append('%.1f'%(100*float(item['agents_detail'])/item['car_detail']))	
	return render(request,"car_conversion.htm",{'select_date':json.dumps(select_date),'car_tab':json.dumps(car_tab),'car_summary':json.dumps(car_summary),\
	'car_detail':json.dumps(car_detail),'agents_detail':json.dumps(agents_detail),'agents_inquiry':json.dumps(agents_inquiry),'form':form,'result':Dict,'date_format':date_format,\
	'a2b':json.dumps(a2b),'b2c':json.dumps(b2c),'c2d':json.dumps(c2d)})

	


@permission_required('push.app_channel', login_url='/push/push_login/')
def app_channel(request):
	if request.POST:
		form=ChannelForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			ob_format=form.cleaned_data['ob_format']
			if ob_format=='add':
				Dict = serializers.serialize("json", Channel.objects.filter(date__gte=start_date,date__lte=end_date).order_by('date'))
				Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
				select_date=[]
				exact_list=[]
				c11_list=[]
				c32_list=[]
				c37_list=[]
				c49_list=[]
				c53_list=[]
				c7_list=[]
				c8_list=[]
				c9_list=[]
				free_list=[]
				ios_list=[]
				for item in Dict:
					if item['channel']=='exact':
						select_date.append(item['date'])
						exact_list.append(item['install'])
					elif item['channel']=='c11':
						c11_list.append(item['install'])
					elif item['channel']=='c32':
						c32_list.append(item['install'])
					elif item['channel']=='c37':
						c37_list.append(item['install'])
					elif item['channel']=='c49':
						c49_list.append(item['install'])
					elif item['channel']=='c53':
						c53_list.append(item['install'])
					elif item['channel']=='c7':
						c7_list.append(item['install'])
					elif item['channel']=='c8':
						c8_list.append(item['install'])
					elif item['channel']=='c9':
						c9_list.append(item['install'])
					elif item['channel']=='free':
						free_list.append(item['install'])	
					elif item['channel']=='ios':
						ios_list.append(item['install'])	
				new_list=[]
				new_dict=[]
				mid=map(list,zip(select_date,exact_list,c11_list,c32_list,c37_list,c49_list,c53_list,c7_list,c8_list,c9_list,free_list,ios_list))
				for item in mid:
					new_dict=dict(zip(['date','exact','c11','c32','c37','c49','c53','c7','c8','c9','free','ios'],item))
					new_list.append(new_dict)
			else:
				Dict = serializers.serialize("json", Channel.objects.filter(date__gte=start_date,date__lte=end_date).order_by('date'))
				Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
				select_date=[]
				exact_list=[]
				c11_list=[]
				c32_list=[]
				c37_list=[]
				c49_list=[]
				c53_list=[]
				c7_list=[]
				c8_list=[]
				c9_list=[]
				free_list=[]
				ios_list=[]
				for item in Dict:
					if item['channel']=='exact':
						select_date.append(item['date'])
						exact_list.append(item['active_user'])
					elif item['channel']=='c11':
						c11_list.append(item['active_user'])
					elif item['channel']=='c32':
						c32_list.append(item['active_user'])
					elif item['channel']=='c37':
						c37_list.append(item['active_user'])
					elif item['channel']=='c49':
						c49_list.append(item['active_user'])
					elif item['channel']=='c53':
						c53_list.append(item['active_user'])
					elif item['channel']=='c7':
						c7_list.append(item['active_user'])
					elif item['channel']=='c8':
						c8_list.append(item['active_user'])
					elif item['channel']=='c9':
						c9_list.append(item['active_user'])
					elif item['channel']=='free':
						free_list.append(item['active_user'])	
					elif item['channel']=='ios':
						ios_list.append(item['active_user'])
				new_list=[]
				new_dict=[]
				mid=map(list,zip(select_date,exact_list,c11_list,c32_list,c37_list,c49_list,c53_list,c7_list,c8_list,c9_list,free_list,ios_list))
				for item in mid:
					new_dict=dict(zip(['date','exact','c11','c32','c37','c49','c53','c7','c8','c9','free','ios'],item))
					new_list.append(new_dict)
			return render(request,"app_channel.htm",{'select_date':json.dumps(select_date),'exact_list':json.dumps(exact_list),'c11_list':json.dumps(c11_list),\
			'c32_list':json.dumps(c32_list),'c37_list':json.dumps(c37_list),'c49_list':json.dumps(c49_list),'c53_list':json.dumps(c53_list),'c7_list':json.dumps(c7_list),\
			'c8_list':json.dumps(c8_list),'c9_list':json.dumps(c9_list),'free_list':json.dumps(free_list),'ios_list':json.dumps(ios_list),'form':form,'result':new_list})

				
	else:# 当正常访问时
		form = ChannelForm()
		Dict = serializers.serialize("json", Channel.objects.filter(date__gte=start_init.strftime('%Y-%m-%d'),date__lte=end_init.strftime('%Y-%m-%d')).order_by('date'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		select_date=[]
		exact_list=[]
		c11_list=[]
		c32_list=[]
		c37_list=[]
		c49_list=[]
		c53_list=[]
		c7_list=[]
		c8_list=[]
		c9_list=[]
		free_list=[]
		ios_list=[]
		for item in Dict:
			if item['channel']=='exact':
				select_date.append(item['date'])
				exact_list.append(item['install'])
			elif item['channel']=='c11':
				c11_list.append(item['install'])
			elif item['channel']=='c32':
				c32_list.append(item['install'])
			elif item['channel']=='c37':
				c37_list.append(item['install'])
			elif item['channel']=='c49':
				c49_list.append(item['install'])
			elif item['channel']=='c53':
				c53_list.append(item['install'])
			elif item['channel']=='c7':
				c7_list.append(item['install'])
			elif item['channel']=='c8':
				c8_list.append(item['install'])
			elif item['channel']=='c9':
				c9_list.append(item['install'])
			elif item['channel']=='free':
				free_list.append(item['install'])	
			elif item['channel']=='ios':
				ios_list.append(item['install'])
			new_list=[]
			new_dict=[]
			mid=map(list,zip(select_date,exact_list,c11_list,c32_list,c37_list,c49_list,c53_list,c7_list,c8_list,c9_list,free_list,ios_list))
			for item in mid:
				new_dict=dict(zip(['date','exact','c11','c32','c37','c49','c53','c7','c8','c9','free','ios'],item))
				new_list.append(new_dict)
	return render(request,"app_channel.htm",{'select_date':json.dumps(select_date),'exact_list':json.dumps(exact_list),'c11_list':json.dumps(c11_list),\
	'c32_list':json.dumps(c32_list),'c37_list':json.dumps(c37_list),'c49_list':json.dumps(c49_list),'c53_list':json.dumps(c53_list),'c7_list':json.dumps(c7_list),\
	'c8_list':json.dumps(c8_list),'c9_list':json.dumps(c9_list),'free_list':json.dumps(free_list),'ios_list':json.dumps(ios_list),'form':form,'result':new_list})

@permission_required('push.app_stay', login_url='/push/push_login/')	
def app_stay(request):
	date_format='date'
	if request.POST:
		form=AppStayForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			platform=form.cleaned_data['platform']
			if platform=='total':
				Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='appstay').order_by('dt'))
				Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
				key_list=['AppUseTime','AndroidUseTime','IosUseTime','SingleUseTime','AndroidSingleUseTime','IosSingleUseTime']
				key_list_cn=['app日均','adr日均','ios日均','app单次','adr单次','ios单次']

				data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
				return render(request,"push_line.htm",data_set)
			
			elif platform=='part':
				Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='appstay').order_by('dt'))
				Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
				key_list=['TabTouTiao','TabCheYou','TabXuanChe','TabHuoDong','TabWoDe']
				key_list_cn=['头条','社区','选车','服务','我的']
				data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
				return render(request,"push_line.htm",data_set)
						
	else:# 当正常访问时
		form = AppStayForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='appstay').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		key_list=['AppUseTime','AndroidUseTime','IosUseTime','SingleUseTime','AndroidSingleUseTime','IosSingleUseTime']
		key_list_cn=['app日均','adr日均','ios日均','app单次','adr单次','ios单次']
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,"push_line.htm",data_set)

@permission_required('push.app_core', login_url='/push/push_login/')
def app_core(request):
	date_format='date'
	if request.POST:
		form=AppIndexForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			key_list=form.cleaned_data['key_list']
			target_format=form.cleaned_data['target_format']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='log_basic').order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			key_list_cn=tran_keys(key_list)
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
			return render(request,'push_line.htm',data_set)
	else:
		form=AppIndexForm()
		key_list=['active','newadd','login']
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='log_basic').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		key_list_cn=tran_keys(key_list)
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,'push_line.htm',data_set)

@permission_required('push.app_core2', login_url='/push/push_login/')
def app_core2(request):
	date_format='date'
	if request.POST:
		form=AppIndexSingleForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			key=form.cleaned_data['key_list']
			key_list=[]
			key_list.append(key)
			target_format=form.cleaned_data['target_format']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='log_module').order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			key_list_cn=tran_keys(key_list)
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
			return render(request,'push_line.htm',data_set)
	else:
		form=AppIndexSingleForm()
		key_list=['headline']
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='log_module').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		key_list_cn=tran_keys(key_list)
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,'push_line.htm',data_set)

	
# @permission_required('push.add_AppIndex', login_url='/push/push_login/')
# def app_pageview(request):
	# key_list=['news_all','news','media','album','video','live','videoplay','post','carmodel']
	# key_list_cn=tran_keys(key_list)
	# date_format='date'
	# if request.POST:
		# form=PushForm(request.POST)
		# if form.is_valid():
			# start_date=form.cleaned_data['start_date']
			# end_date=form.cleaned_data['end_date']
			# Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key__in=key_list,c_type='pv').order_by('dt'))
			# Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			# data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
			# return render(request,'push_line.htm',data_set)
	# else:
		# form=PushForm()
		# Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key__in=key_list,c_type='pv').order_by('dt'))
		# Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		# data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	# return render(request,'push_line.htm',data_set)

@permission_required('push.business', login_url='/push/push_login/')
def business(request):
	key_list=['askprice','askpriceok','loan','loan_ok','buynewcar','buycar_ok','replace','replace_ok']
	key_list_cn=tran_keys(key_list)
	date_format='date'
	if request.POST:
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='log_business').order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
			return render(request,'push_line.htm',data_set)
	else:
		form=PushForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='log_business').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,'push_line.htm',data_set)
	
	
#@login_required(login_url='/push/push_login/')	
@permission_required('push.app_retain', login_url='/push/push_login/')
def app_retain(request):
	key_list=['adr_retain','ios_retain']
	key_list_cn=['adr留存','ios留存']
	date_format='date'
	if request.POST:
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='newuser_retain').order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
			return render(request,"push_line.htm",data_set)

				
	else:# 当正常访问时
		form = PushForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='newuser_retain').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,"push_line.htm",data_set)

@permission_required('push.add_appindex', login_url='/push/push_login/')
def app_tem(request,chart_key):
	last_type=request.session.get('last_type','null')
	logger.info('type=%s&user=%s&ip=%s&last_type=%s' %(request.path_info,request.user.username,request.META['REMOTE_ADDR'],last_type))
	request.session['last_type']=request.path_info
	date_format='date'
	data=AppChart.objects.filter(chart_key=chart_key).values('chart_list','chart_list_cn')
	key_list=eval(list(data)[0]['chart_list'])
	key_list_cn=eval(list(data)[0]['chart_list_cn'])
	summary_chart=AppChart.objects.filter(chart_column='summary')
	headline_chart=AppChart.objects.filter(chart_column='headline')
	community_chart=AppChart.objects.filter(chart_column='community')
	car_chart=AppChart.objects.filter(chart_column='car')
	nav_dict={'summary_chart':summary_chart,'headline_chart':headline_chart,'community_chart':community_chart,'car_chart':car_chart}
	if request.method == "GET":
		form = PushForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key=chart_key).order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
		data_set=dict(data_set,**nav_dict)
		return render(request,"push_line2.htm",data_set)

	elif request.method == "POST":
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key=chart_key).order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
			data_set=dict(data_set,**nav_dict)
		return render(request,"push_line2.htm",data_set)

				
	

@permission_required('push.app_active', login_url='/push/push_login/')
def app_active(request):
	last_type=request.session.get('last_type','null')
	logger.info('type=%s&user=%s&ip=%s&last_type=%s' %(request.path_info,request.user.username,request.META['REMOTE_ADDR'],last_type))
	request.session['last_type']=request.path_info
	date_format='date'
	data=AppChart.objects.filter(chart_key='ym_active').values('chart_list','chart_list_cn')
	key_list=eval(list(data)[0]['chart_list'])
	key_list_cn=eval(list(data)[0]['chart_list_cn'])
	if request.POST:
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='ym_active').order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
			return render(request,"push_line.htm",data_set)

				
	else:# 当正常访问时
		form = PushForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='ym_active').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,"push_line.htm",data_set)

#@login_required(login_url='/push/push_login/')	
@permission_required('push.app_add', login_url='/push/push_login/')
def app_add(request):
	last_type=request.session.get('last_type','null')
	logger.info('type=%s&user=%s&ip=%s&last_type=%s' %(request.path_info,request.user.username,request.META['REMOTE_ADDR'],last_type))
	request.session['last_type']=request.path_info
	key_list=['adr_add','ios_add','ipad_add']
	key_list_cn=['adr新增','ios新增','ipad新增']
	date_format='date'
	if request.POST:
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='ym_add').order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
			return render(request,"push_line.htm",data_set)

				
	else:# 当正常访问时
		form = PushForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='ym_add').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,"push_line.htm",data_set)

#@login_required(login_url='/push/push_login/')	
@permission_required('push.app_starts', login_url='/push/push_login/')
def app_starts(request):
	key_list=['adr_starts','ios_starts','ipad_starts']
	key_list_cn=['adr启动次数','ios启动次数','ipad启动次数']
	date_format='date'
	if request.POST:
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_date,dt__lte=end_date,c_key='ym_starts').order_by('dt'))
			Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
			data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
			return render(request,"push_line.htm",data_set)

				
	else:# 当正常访问时
		form = PushForm()
		Dict = serializers.serialize("json", AppIndex.objects.filter(dt__gte=start_init.strftime('%Y-%m-%d'),dt__lte=end_init.strftime('%Y-%m-%d'),c_key='ym_starts').order_by('dt'))
		Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
		data_set=data_format3(key_list,key_list_cn,date_format,Dict,form)
	return render(request,"push_line.htm",data_set)	

#@login_required(login_url='/push/push_login/')	
@permission_required('push.add_appfunnel', login_url='/push/push_login/')
def app_funnel(request):
	if request.POST:
		form=AfterOpenForm(request.POST)
		if form.is_valid():
			submit=form.cleaned_data['create_date']
			Dict = serializers.serialize("json", AppFunnel.objects.filter(date=submit))
			d_list=list(map(lambda x:x['fields'],json.loads(Dict)))
			legend_data=['浏览','交互','商机']
			data=[]
			percent_data=[]
			dict1={}
			dict2={}
			dict3={}
			dict21={}
			dict22={}
			dict23={}
			dict1['value']=d_list[0]['browse']
			dict1['name']='浏览'
			dict2['value']=d_list[0]['interactive']
			dict2['name']='交互'
			dict3['value']=d_list[0]['business']
			dict3['name']='商机'
			data.append(dict1)
			data.append(dict2)
			data.append(dict3)
			dict21['value']=d_list[0]['browse']
			dict22['value']=d_list[0]['interactive']
			dict23['value']=d_list[0]['business']
			dict21['value']=100
			dict22['value']=100*d_list[0]['interactive']/d_list[0]['browse']
			dict23['value']=100*d_list[0]['business']/d_list[0]['browse']
			percent_data.append(dict21)
			percent_data.append(dict22)
			percent_data.append(dict23)
			return render(request,"app_funnel.htm",{'data':json.dumps(data),'percent_data':json.dumps(percent_data),'legend':json.dumps(legend_data),'form':form})

				
	else:# 当正常访问时
		form = AfterOpenForm()
		Dict = serializers.serialize("json", AppFunnel.objects.filter(date=end_init.strftime('%Y-%m-%d')))
		d_list=list(map(lambda x:x['fields'],json.loads(Dict)))
		legend_data=['浏览','交互','商机']
		data=[]
		percent_data=[]
		dict1={}
		dict2={}
		dict3={}
		dict21={}
		dict22={}
		dict23={}
		dict1['value']=d_list[0]['browse']
		dict1['name']='浏览'
		dict2['value']=d_list[0]['interactive']
		dict2['name']='交互'
		dict3['value']=d_list[0]['business']
		dict3['name']='商机'
		data.append(dict1)
		data.append(dict2)
		data.append(dict3)
		dict21['value']=d_list[0]['browse']
		dict22['value']=d_list[0]['interactive']
		dict23['value']=d_list[0]['business']
		dict21['value']=100
		dict22['value']=100*d_list[0]['interactive']/d_list[0]['browse']
		dict23['value']=100*d_list[0]['business']/d_list[0]['browse']
		percent_data.append(dict21)
		percent_data.append(dict22)
		percent_data.append(dict23)
	return render(request,"app_funnel.htm",{'data':json.dumps(data),'percent_data':json.dumps(percent_data),'legend':json.dumps(legend_data),'form':form})



	

#@login_required(login_url='/push/push_login/')	
@permission_required('push.add_lossactive', login_url='/push/push_login/')
def loss_active(request):
	Dict = serializers.serialize("json", LossActive.objects.all())
	d_list=list(map(lambda x:x['fields'],json.loads(Dict)))
	content=[]
	for item in d_list:
		item['rate']='%.2f' % (100*float(item['open_num'])/item['push_num'])+'%'
		content.append(item)
	content=sorted(content,key=lambda x:x['create_date'])
	return render(request,'loss_active.htm',{'result':content})

#@login_required(login_url='/push/push_login/')	
@permission_required('push.add_push', login_url='/push/push_login/')
def push_content(request):
	if request.POST:
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict = serializers.serialize("json", Push.objects.filter(push_date__gte=start_date,push_date__lte=end_date))
			d_list=list(map(lambda x:x['fields'],json.loads(Dict)))
			d_list=sorted(d_list,key=lambda x:x['open_rate'])
			top_content=[]
			tail_content=[]
			adr_mid=[]
			ios_mid=[]
			e_list=[]
			for item in d_list:
				item['rate']='%.2f' % (100*float(item['open_num'])/item['push_num'])+'%'
				e_list.append(item)
			for item in e_list:
				if item['platform'].strip() =='ADR':
					adr_mid.append(item)
				else:
					ios_mid.append(item)
			top_content=adr_mid[-5:]+ios_mid[-5:]
			tail_content=adr_mid[:5]+ios_mid[:5]
			top_content=sorted(top_content,key=lambda x:x['platform'])
			tail_content=sorted(tail_content,key=lambda x:x['platform'])
			return render(request,'push_content.htm',locals())
	else:
		form=PushForm()
		Dict = serializers.serialize("json", Push.objects.filter(push_date__gte='2016-09-19',push_date__lte='2016-09-25'))
		d_list=list(map(lambda x:x['fields'],json.loads(Dict)))
		d_list=sorted(d_list,key=lambda x:x['open_rate'])
		top_content=[]
		tail_content=[]
		adr_mid=[]
		ios_mid=[]
		e_list=[]
		for item in d_list:
			item['rate']='%.2f' % (100*float(item['open_num'])/item['push_num'])+'%'
			e_list.append(item)
		for item in e_list:
			if item['platform'].strip() =='ADR':
				adr_mid.append(item)
			else:
				ios_mid.append(item)
		top_content=adr_mid[-5:]+ios_mid[-5:]
		tail_content=adr_mid[:5]+ios_mid[:5]
		top_content=sorted(top_content,key=lambda x:x['platform'])
		tail_content=sorted(tail_content,key=lambda x:x['platform'])
	return render(request,'push_content.htm',locals())
	


#@login_required(login_url='/push/push_login/')	
@permission_required('push.add_areaactive', login_url='/push/push_login/')
def area_active(request):
	if request.POST:
		form=AfterOpenForm(request.POST)
		if form.is_valid():
			submit=form.cleaned_data['create_date']
			Dict = serializers.serialize("json", AreaActive.objects.filter(create_date=submit))
			d_list=list(map(lambda x:x['fields'],json.loads(Dict)))
			data3=[]
			for item in d_list:
				dict={}
				dict['name']=item['province']
				dict['value']=item['push_click']
				data3.append(dict)	

			return render(request,'area_active.htm',{'data3':json.dumps(data3),'form':form})

				
	else:# 当正常访问时
		form = AfterOpenForm()
		Dict = serializers.serialize("json", AreaActive.objects.filter(create_date=end_init.strftime('%Y-%m-%d')))
		d_list=list(map(lambda x:x['fields'],json.loads(Dict)))
		data3=[]
		for item in d_list:
			dict={}
			dict['name']=item['province']
			dict['value']=item['push_click']
			data3.append(dict)
	return render(request,'area_active.htm', {'data3':json.dumps(data3),'form':form})

#@login_required(login_url='/push/push_login/')	
@permission_required('push.add_push', login_url='/push/push_login/')
def push_send(request):
	if request.POST:
		form=PushSendForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			platform=form.cleaned_data['platform']
			Dict = Push.objects.filter(push_date__gte=start_date,push_date__lte=end_date,platform=platform).values('push_date','platform').annotate(push_num=Sum('push_num'),open_num=Sum('open_num')).order_by('push_date')
			Legend=['发送数','打开数','打开率']
			Axis=[]
			push_num=[]
			open_num=[]
			open_rate=[]
			for item in Dict:
				Axis.append(item['push_date'])
				push_num.append(item['push_num'])
				open_num.append(item['open_num'])
				open_rate.append('%.2f'%(100*item['open_num']/float(item['push_num'])))
				
			return render(request,'push_send.htm',{'list1':json.dumps(push_num),'list2':json.dumps(open_num),'list3':json.dumps(open_rate),'Legend':json.dumps(Legend),'Axis':json.dumps(Axis, cls=CJsonEncoder),'form':form})
				
	else:# 当正常访问时
		form = PushSendForm()
		Dict = Push.objects.filter(push_date__gte='2016-08-15',push_date__lte=end_init.strftime('%Y-%m-%d'),platform='ADR').values('push_date','platform').annotate(push_num=Sum('push_num'),open_num=Sum('open_num')).order_by('push_date')
		Legend=['发送数','打开数','打开率']
		Axis=[]
		push_num=[]
		open_num=[]
		open_rate=[]	
		for item in Dict:
			Axis.append(item['push_date'])
			push_num.append(item['push_num'])
			open_num.append(item['open_num'])
			open_rate.append('%.2f'%(100*item['open_num']/float(item['push_num'])))
	return render(request,'push_send.htm', {'list1':json.dumps(push_num),'list2':json.dumps(open_num),'list3':json.dumps(open_rate),'Legend':json.dumps(Legend),'Axis':json.dumps(Axis, cls=CJsonEncoder),'form':form})


#@login_required(login_url='/push/push_login/')	
@permission_required('push.add_pushactive', login_url='/push/push_login/')
def push_active(request):
	if request.POST:
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict = serializers.serialize("json", PushActive.objects.filter(create_date__gte=start_date,create_date__lte=end_date))
			d_list=list(map(lambda x:x['fields'],json.loads(Dict)))
			d_list=sorted(d_list,key=lambda x:x['create_date'])
			Legend=['push点击','push点击&首次活跃','首次活跃比']
			Axis=[x['create_date'] for x in d_list]
			Axis=list(set(Axis))
			Axis=sorted(Axis)
			list1=[]
			list2=[]
			list3=[]	
			for item in d_list:
				list1.append(item['push_num'])
				list2.append(item['active_num'])
				list3.append(100*item['active_num']/item['push_num'])
				
			return render(request,'push_active.htm',{'list1':json.dumps(list1),'list2':json.dumps(list2),'list3':json.dumps(list3),'Legend':json.dumps(Legend),'Axis':json.dumps(Axis),'form':form})
				
	else:# 当正常访问时
		form = PushForm()
		Dict = serializers.serialize("json", PushActive.objects.filter(create_date__gte='2016-08-15',create_date__lte=end_init.strftime('%Y-%m-%d')))
		d_list=list(map(lambda x:x['fields'],json.loads(Dict)))
		d_list=sorted(d_list,key=lambda x:x['create_date'])
		Legend=['push点击','push点击&首次活跃','首次活跃比']
		Axis=[x['create_date'] for x in d_list]
		Axis=list(set(Axis))
		Axis=sorted(Axis)
		list1=[]
		list2=[]
		list3=[]	
		for item in d_list:
			list1.append(item['push_num'])
			list2.append(item['active_num'])
			list3.append(100*item['active_num']/item['push_num'])
	return render(request,'push_active.htm', {'list1':json.dumps(list1),'list2':json.dumps(list2),'list3':json.dumps(list3),'Legend':json.dumps(Legend),'Axis':json.dumps(Axis),'form':form})

#@login_required(login_url='/push/push_login/')	
@permission_required('push.add_pushclick', login_url='/push/push_login/')
def push_click(request):
	if request.POST:
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict = serializers.serialize("json", PushClick.objects.filter(create_date__gte=start_date,create_date__lte=end_date))
			d_list=list(map(lambda x:x['fields'],json.loads(Dict)))
			d_list=sorted(d_list,key=lambda x:x['create_date'])
			Legend=['一次','两次','三次及以上']
			Axis=[x['create_date'] for x in d_list]
			Axis=list(set(Axis))
			Axis=sorted(Axis)
			list1=[]
			list2=[]
			list3=[]	
			for item in d_list:
				list1.append(item['onetimes'])
				list2.append(item['twotimes'])
				list3.append(item['threetimes'])
				
			return render(request,'push_click.htm',{'list1':json.dumps(list1),'list2':json.dumps(list2),'list3':json.dumps(list3),'Legend':json.dumps(Legend),'Axis':json.dumps(Axis),'form':form})
				
	else:# 当正常访问时
		form = PushForm()
		Dict = serializers.serialize("json", PushClick.objects.filter(create_date__gte='2016-08-15',create_date__lte=end_init.strftime('%Y-%m-%d')))
		d_list=list(map(lambda x:x['fields'],json.loads(Dict)))
		d_list=sorted(d_list,key=lambda x:x['create_date'])
		Legend=['一次','两次','三次及以上']
		Axis=[x['create_date'] for x in d_list]
		Axis=list(set(Axis))
		Axis=sorted(Axis)
		list1=[]
		list2=[]
		list3=[]	
		for item in d_list:
			list1.append(item['onetimes'])
			list2.append(item['twotimes'])
			list3.append(item['threetimes'])
	return render(request,'push_click.htm', {'list1':json.dumps(list1),'list2':json.dumps(list2),'list3':json.dumps(list3),'Legend':json.dumps(Legend),'Axis':json.dumps(Axis),'form':form})

#@login_required(login_url='/push/push_login/')	
@permission_required('push.add_afteropen', login_url='/push/push_login/')
def after_open(request):
	if request.POST:
		form=AfterOpenForm(request.POST)
		if form.is_valid():
			submit=form.cleaned_data['create_date']
			Dict = serializers.serialize("json", AfterOpen.objects.filter(create_date=submit))
			d_list=list(map(lambda x:x['fields'],json.loads(Dict)))
			inner_data=[]
			outer_data=[]
			legend_data=[]
			for item in d_list:
				inner_dict={}
				outer_dict={}
				inner_dict['name']=item['name1']
				inner_dict['value']=item['value1']
				outer_dict['name']=item['name2']
				outer_dict['value']=item['value2']
				legend_data.append(item['name1'])
				legend_data.append(item['name2'])
				inner_data.append(inner_dict)
				outer_data.append(outer_dict)
			new_inner=[]
			for item in inner_data:
				if item not in new_inner:
					new_inner.append(item)
			legend_data=list(set(legend_data))
			return render(request,"after_open.htm",{'inner_data':json.dumps(new_inner),'outer_data':json.dumps(outer_data),'legend_data':json.dumps(legend_data),'form':form})

				
	else:# 当正常访问时
		form = AfterOpenForm()
		Dict = serializers.serialize("json", AfterOpen.objects.filter(create_date=end_init.strftime('%Y-%m-%d')))
		d_list=list(map(lambda x:x['fields'],json.loads(Dict)))
		inner_data=[]
		outer_data=[]
		legend_data=[]
		for item in d_list:
			inner_dict={}
			outer_dict={}
			inner_dict['name']=item['name1']
			inner_dict['value']=item['value1']
			outer_dict['name']=item['name2']
			outer_dict['value']=item['value2']
			legend_data.append(item['name1'])
			legend_data.append(item['name2'])
			inner_data.append(inner_dict)
			outer_data.append(outer_dict)
		new_inner=[]
		for item in inner_data:
			if item not in new_inner:
				new_inner.append(item)
		legend_data=list(set(legend_data))
	return render(request,"after_open.htm", {'inner_data':json.dumps(new_inner),'outer_data':json.dumps(outer_data),'legend_data':json.dumps(legend_data),'form':form})

#@login_required(login_url='/push/push_login/')	
@permission_required('push.add_push', login_url='/push/push_login/')
def push_open(request):
	if request.POST:
		form=PushForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			Dict =Push.objects.filter(push_date__gte=start_date,push_date__lte=end_date).values('push_date','platform').annotate(push_num=Sum('push_num'),open_num=Sum('open_num')).order_by('push_date')
			create_date=[]
			adr_rate=[]
			ios_rate=[]
			for item in Dict:
				if item['platform'].strip()=='ADR':
					create_date.append(item['push_date'])
					item['rate']='%.2f'%(100*item['open_num']/float(item['push_num']))
					adr_rate.append(item['rate'])
				else:
					item['rate']='%.2f'%(100*item['open_num']/float(item['push_num']))
					ios_rate.append(item['rate'])
			return render(request,"push_open.htm",{'push_date':json.dumps(create_date, cls=CJsonEncoder),'adr_rate':json.dumps(adr_rate),'ios_rate':json.dumps(ios_rate),'form':form})

				
	else:
		form = PushForm()
		Dict =Push.objects.filter(push_date__gte=start_init.strftime('%Y-%m-%d'),push_date__lte=end_init.strftime('%Y-%m-%d')).values('push_date','platform').annotate(push_num=Sum('push_num'),open_num=Sum('open_num')).order_by('push_date')
		create_date=[]
		adr_rate=[]
		ios_rate=[]
		for item in Dict:
			if item['platform'].strip()=='ADR':
				create_date.append(item['push_date'])
				item['rate']='%.2f'%(100*item['open_num']/float(item['push_num']))
				adr_rate.append(item['rate'])
			else:
				item['rate']='%.2f'%(100*item['open_num']/float(item['push_num']))
				ios_rate.append(item['rate'])
		return render(request,"push_open.htm",{'push_date':json.dumps(create_date, cls=CJsonEncoder),'adr_rate':json.dumps(adr_rate),'ios_rate':json.dumps(ios_rate),'form':form})
def value_label(value):
	return {'posts':'发帖','replies':'回帖','likes':'点赞','attentions':'关注','votes':'投票'}[value]

#@login_required(login_url='/push/push_login/')	
@permission_required('push.add_appposts', login_url='/push/push_login/')	
def data_compare(request):
	if request.POST:
		form=DataCompareForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			date_format=form.cleaned_data['date_format']
			field1=form.cleaned_data['field1']
			field2=form.cleaned_data['field2']
			field3=form.cleaned_data['field3']
			table_head={'name':'检验方法','value':'值','result':'结论'}
			if date_format=='date':
				Dict = serializers.serialize("json", AppPosts.objects.filter(date__gte=start_date,date__lte=end_date))
				Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
				select_date=[]
				index1=[]
				index2=[]
				rate=[]
				t_test={}
				anova={}
				corretion={}
				legend={'field1':value_label(field1),'field2':value_label(field2),'rate':rate}
				for item in Dict:
					select_date.append(item['date'])
					index1.append(item[field1])
					index2.append(item[field2])
					rate.append('%.1f'%(100*float(item[field1])/item[field2]))
				if 't' in field3:
					t=ttest_ind(index1,index2)[1]
					if t<0.05:
						t_result='有显著差异'
					else:
						t_result='无显著差异'
					t_test['name']='t检验:'
					t_test['value']='%.3f'%(ttest_ind(index1,index2)[1])
					t_test['result']=t_result
				if 'anova' in field3:
					args=[index1,index2]
					w,p=stats.levene(*args)
					if p<0.05:
						signal='方差齐性假设不成立,'
					else:
						signal='方差齐性假设成立,'
					f,p=stats.f_oneway(*args)
					if p<0.05:
						a_result='有显著差异'
					else:
						a_result='无显著差异'
					anova['name']='方差分析:'
					anova['levene']=signal
					anova['value']='%.3f'%p
					anova['result']=a_result
				if 'correlation' in field3:
					corr=correlation(index1,index2)
					if abs(corr)>=0.6:
						c_result='强相关'
					elif abs(corr)>=0.3:
						c_result='中等相关'
					elif abs(corr)>=0.1:
						c_result='弱相关'
					else:
						c_result='无相关性'
					corretion['name']='相关系数:'
					corretion['value']='%.3f'%(correlation(index1,index2))
					corretion['result']=c_result
					
			else:
				Dict = AppPosts.objects.filter(date__gte=start_date,date__lte=end_date).values(date_format).annotate(posts=Avg('posts'),replies=Avg('replies'),likes=Avg('likes'),attentions=Avg('attentions'),votes=Avg('votes'))
				select_date=[]
				index1=[]
				index2=[]
				rate=[]
				t_test={}
				anova={}
				corretion={}
				legend={'field1':value_label(field1),'field2':value_label(field2),'rate':rate}
				for item in Dict:
					select_date.append(item[date_format])
					index1.append(item[field1])
					index2.append(item[field2])
					rate.append('%.1f'%(100*float(item[field1])/item[field2]))
				if 't' in field3:
					t=ttest_ind(index1,index2)[1]
					if t<0.05:
						t_result='有显著差异'
					else:
						t_result='无显著差异'
					t_test['name']='t检验:'
					t_test['value']='%.3f'%(ttest_ind(index1,index2)[1])
					t_test['result']=t_result
				if 'anova' in field3:
					args=[index1,index2]
					w,p=stats.levene(*args)
					if p<0.05:
						signal='方差齐性假设不成立,'
					else:
						signal='方差齐性假设成立,'
					f,p=stats.f_oneway(*args)
					if p<0.05:
						a_result='有显著差异'
					else:
						a_result='无显著差异'
					anova['name']='方差分析:'
					anova['levene']=signal
					anova['value']='%.3f'%p
					anova['result']=a_result
				if 'correlation' in field3:
					corr=correlation(index1,index2)
					if abs(corr)>=0.6:
						c_result='强相关'
					elif abs(corr)>=0.3:
						c_result='中等相关'
					elif abs(corr)>=0.1:
						c_result='弱相关'
					else:
						c_result='无相关性'
					corretion['name']='相关系数:'
					corretion['value']='%.3f'%(correlation(index1,index2))
					corretion['result']=c_result
			return render(request,"data_compare.htm",{'legend':legend,'table_head':table_head,'corretion':corretion,'anova':anova,'t_test':t_test,'field3':field3,'select_date':json.dumps(select_date),'index1':json.dumps(index1),'index2':json.dumps(index2),'rate':json.dumps(rate),'form':form})

				
	else:# 当正常访问时
		form = DataCompareForm()
	return render(request,"data_compare.htm",{'form':form})	

#@login_required(login_url='/push/push_login/')	
@permission_required('push.add_appposts', login_url='/push/push_login/')	
def data_regression(request):
	if request.POST:
		form=DataCompareForm(request.POST)
		if form.is_valid():
			start_date=form.cleaned_data['start_date']
			end_date=form.cleaned_data['end_date']
			date_format=form.cleaned_data['date_format']
			field1=form.cleaned_data['field1']
			field2=form.cleaned_data['field2']		
			if date_format=='date':
				Dict = serializers.serialize("json", AppPosts.objects.filter(date__gte=start_date,date__lte=end_date))
				Dict=list(map(lambda x:x['fields'],json.loads(Dict)))
				select_date=[]
				index1=[]
				index2=[]
				for item in Dict:
					select_date.append(item['date'])
					index1.append(float(item[field1]))
					index2.append(float(item[field2]))
				regr=linear_model.LinearRegression()
				regr.fit(list(map(lambda x:[x],index1)),index2)
				a=regr.intercept_
				b=regr.coef_[0]
				formatter_str='''%s =%s + %s * %s '''%(value_label(field2),str(b),str(a),value_label(field1))
				x_min=min(index1)
				x_max=max(index1)
				y_min=regr.predict(x_min)
				y_max=regr.predict(x_max)
				data=map(list,zip(index1,index2,map(lambda x:0.7,range(len(index1)))))
					
			else:
				Dict = AppPosts.objects.filter(date__gte=start_date,date__lte=end_date).values(date_format).annotate(posts=Avg('posts'),replies=Avg('replies'),likes=Avg('likes'),attentions=Avg('attentions'),votes=Avg('votes'))
				select_date=[]
				index1=[]
				index2=[]
				for item in Dict:
					select_date.append(item[date_format])
					index1.append(float(item[field1]))
					index2.append(float(item[field2]))
				regr=linear_model.LinearRegression()
				regr.fit(list(map(lambda x:[x],index1)),index2)
				a=regr.intercept_
				b=regr.coef_[0]
				formatter_str='''%s =%s + %s * %s '''%(value_label(field2),str(b),str(a),value_label(field1))
				x_min=min(index1)
				x_max=max(index1)
				y_min=regr.predict(x_min)
				y_max=regr.predict(x_max)
				data=map(list,zip(index1,index2,map(lambda x:0.7,range(len(index1)))))

			return render(request,"data_regression.htm",{'data':json.dumps(data),'x_min':x_min,'x_max':x_max,'y_min':y_min[0],'y_max':y_max[0],'formatter_str':formatter_str,'form':form})
				
	else:# 当正常访问时
		form = DataCompareForm()
	return render(request,"data_regression.htm",{'form':form})	
