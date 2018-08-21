# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import json
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your models here.
# 9.20add replace_click,replace car_inquiry to car_inquiry_pv
class ListField(models.TextField):
	description = "List"
	def __init__(self, *args, **kwargs):
		super(ListField,self).__init__(*args,**kwargs)
	
	def to_python(self,value):
		if not value:
			value=[]
		if isinstance(value,list):
			return value
		import ast
		return ast.literal_eval(value)

	def get_prep_value(self, value):
		if value is None:
			return value
		return unicode(value)
	def value_to_string(self, obj):
		value = self._get_val_from_obj(obj)
		return self.get_db_prep_value(value)

class JSONField(models.TextField):  
	description = "Json"  
	def to_python(self, value):  
		v = models.TextField.to_python(self, value)  
		try:  
			return json.loads(v)['v']  
		except:  
			pass  
		return v  
	def get_prep_value(self, value):  
		return json.dumps({'v':value})

class TypeSet(models.Model):
	type_name=models.CharField(max_length=40)
	type_desc=models.CharField(max_length=40)
	def __unicode__(self):
		return self.type_desc

class PageSet(models.Model):
	module_name=models.CharField(max_length=40)
	page_name=models.CharField(max_length=40)
	page_desc=models.CharField(max_length=40)
	def __unicode__(self):
		return self.page_desc
	class Meta:
		ordering =['-page_desc']

class ViewSet(models.Model):
	view_name=models.CharField(max_length=20)
	view_desc=models.CharField(max_length=20)
	def __unicode__(self):
		return self.view_desc

class ObjectSet(models.Model):
	object_name=models.CharField(max_length=20)
	object_desc=models.CharField(max_length=20)
	def __unicode__(self):
		return self.object_desc

class AppVersion(models.Model):
	version=models.CharField(max_length=10)
	version_dt=models.DateField(null=True,blank=True)
	def __unicode__(self):
		return self.version

class LogList(models.Model):
	version=models.ForeignKey(AppVersion,help_text='必需*',verbose_name='版本号')
	user_name=models.ForeignKey(User,help_text='必需*',verbose_name='用户名')
	type_desc=models.CharField(max_length=40,help_text='必需*',verbose_name='事件名')
	type_name=models.ForeignKey(TypeSet,help_text='必需*',verbose_name='type')
	page_name=models.ForeignKey(PageSet,help_text='用户行为所在页面，必需*',verbose_name='页面')
	object_type=models.ForeignKey(ObjectSet,help_text='对象类型，必需*',default=14,verbose_name='对象')
	view_name=models.ForeignKey(ViewSet,help_text='必需*',verbose_name='视图类型')
	dt=models.BigIntegerField(blank=True,default=1480582478509,help_text='必需*',verbose_name='时间')
	column_name=models.CharField(max_length=20,blank=True,null=True,verbose_name='栏目')
	section_name=models.CharField(max_length=20,blank=True,null=True,verbose_name='段落')
	object_name=models.CharField(max_length=20,blank=True,null=True,verbose_name='name',help_text='若对象为其他,则Name不可为空*')
	object_id=models.IntegerField(blank=True,null=True,verbose_name='对象id')
	tlsc=models.IntegerField(blank=True,null=True,verbose_name='停留时长')
	source=models.CharField(blank=True,null=True,max_length=20,verbose_name='来源')
	remark=models.CharField(max_length=40,blank=True,null=True,verbose_name='备注')
	
	def get_json(self):
		tmp_list=[]
		tmp_dict={}
		tmp_dict['type']=self.type_name.type_name
		tmp_dict['page']=self.page_name.page_name
		tmp_dict['objecttype']=self.object_type.object_name
		tmp_dict['viewtype']=self.view_name.view_name
		tmp_dict['dt']=self.dt
		tmp_dict['column']=self.column_name
		tmp_dict['section']=self.section_name
		tmp_dict['name']=self.object_name
		tmp_dict['id']=self.object_id
		tmp_dict['tlsc']=self.tlsc
		tmp_dict['source']=self.source
		for key,value in tmp_dict.items():
			if value=='' or value==None or value=='':
				tmp_dict.pop(key)
		tmp_list.append(tmp_dict)
		return json.dumps(tmp_list,ensure_ascii=False).decode('utf8')
		

class AppChart(models.Model):
	chart_desc=models.CharField(max_length=40)
	chart_key=models.CharField(max_length=20,default='')
	chart_list=ListField()
	chart_list_cn=ListField(default='')
	chart_column=models.CharField(max_length=20,default='summary')

	def get_absolute_url(self):
		return reverse('app_tem', args=(self.chart_key,))

class AppDaily(models.Model):
	daily_key=models.CharField(max_length=40,primary_key=True)
	daily_desc=models.CharField(max_length=40)
	daily_emails=models.ManyToManyField(User)
	def __unicode__(self):
		return self.daily_desc
class AppOperate(models.Model):
	dt=models.DateField()
	c_key=models.CharField(max_length=30)
	c_value=JSONField()

class AppIndex(models.Model):
	dt=models.DateField()
	c_key=models.CharField(max_length=30)
	c_value=JSONField()
	class Meta:
		permissions=(
		("app_active","Can visit app_active"),
		("app_add","Can visit app_add"),
		("app_retain","Can visit app_retain"),
		("app_starts","Can visit app_starts"),
		("app_channel","Can visit app_channel"),
		("moduleuser","Can visit moduleuser"),
		("app_stay","Can visit app_stay"),
		("app_core","Can visit app_core"),
		("app_core2","Can visit app_core2"),
		("business","Can visit business"),
		("app_business","Can visit app_business"),
		("app_video","Can visit app_video"),
		("app_media","Can visit app_media"),
		("news_data","Can visit news_data"),
		("posts_app","Can visit posts_app"),
		("post_detail","Can visit post_dtail"),
		("car_coin","Can visit car_coin"),
		)


class Channel(models.Model):
	date=models.DateField()
	channel=models.CharField(max_length=20)
	install=models.IntegerField()
	active_user=models.IntegerField()
	platform=models.CharField(max_length=10)


class AppKey(models.Model):
	c_key=models.CharField(max_length=20)
	c_desc=models.CharField(max_length=40)
	def __unicode__(self):
		return self.c_desc



class AppBusiness(models.Model):
	yipai = models.IntegerField()
	yixin = models.IntegerField()
	huimaiche    = models.IntegerField()
	yichehui=models.IntegerField()
	ershouche=models.IntegerField()
	week=models.CharField(max_length=20)
	month=models.CharField(max_length=20)
	date=models.DateField()	
	

class AppFunnel(models.Model):
	browse = models.IntegerField()
	interactive = models.IntegerField()
	business    = models.IntegerField()
	date=models.DateField()	
	


class CarConversion(models.Model):
	car_tab=models.IntegerField()
	car_summary=models.IntegerField()
	car_detail=models.IntegerField()
	agents_detail=models.IntegerField()
	agents_inquiry=models.IntegerField()
	week=models.CharField(max_length=20)
	month=models.CharField(max_length=20)
	date=models.DateField()



class UserList(models.Model):
	username = models.CharField(max_length=20)
	password=models.CharField(max_length=20)
	
	# def __unicode__(self):
		# return self.userid

class LossActive(models.Model):
	platform = models.CharField(max_length=20)
	push_num=models.IntegerField()
	open_num=models.IntegerField()
	create_date=models.DateField()
	
	# def __unicode__(self):
		# return self.create_date

class AreaActive(models.Model):
	province = models.CharField(max_length=20,default='')
	push_click= models.IntegerField()
	create_date=models.DateField()
	
	# def __unicode__(self):
		# return self.province	

class PushActive(models.Model):
	push_num = models.IntegerField()
	active_num= models.IntegerField()
	create_date=models.DateField()
	
	# def __unicode__(self):
		# return self.create_date	

class PushClick(models.Model):
	onetimes = models.IntegerField()
	twotimes= models.IntegerField()
	threetimes = models.IntegerField()
	create_date=models.DateField()
	
	# def __unicode__(self):
		# return self.create_date	

class AfterOpen(models.Model):
	name1 = models.CharField(max_length=20,default='')
	value1= models.IntegerField()
	name2 = models.CharField(max_length=20,default='')
	value2= models.IntegerField()
	create_date=models.DateField()
	
	# def __unicode__(self):
		# return self.create_date	

class Push(models.Model):
	news_id = models.CharField(max_length=20)
	content = models.TextField(default='', blank=True)
	title = models.CharField(max_length=40)
	create_time = models.DateTimeField(auto_now_add=True, editable=True)
	platform = models.CharField(max_length=20)
	push_num=models.IntegerField()
	open_num=models.IntegerField()
	push_date=models.DateField()
	push_time=models.CharField(max_length=10)
	open_rate=models.DecimalField(default=0.0, max_digits=5, decimal_places=3)

	
	# def __unicode__(self):
		# return self.title	


