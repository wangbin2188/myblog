# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from push.models import Push,AfterOpen,PushClick,PushActive,AreaActive,UserList,CarConversion
from push.models import AppFunnel,AppBusiness
from push.models import Channel,AppIndex,AppKey,TypeSet,PageSet,ViewSet
from django.contrib.auth.models import User
from django import forms
from django.forms import widgets
from datetime import datetime,timedelta
import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 
# Create your models here.

CHOICES = ( 
    ('date' , u"按天"), 
    ('week' , u"按周"),         
    ('month', u"按月"),    
) 
DAILY_CHOICES = ( 
    ('car_daily' , u"选车日报"), 
    ('headline_daily' , u"头条日报"),         
) 
NEWS_CHOICES = ( 
    ('news' , u"要闻"), 
    ('ycnews' , u"易车新闻"),
    ('video', u"易车视频"), 
	('album' , u"图集"), 
    ('medianews' , u"自媒体"),         
    ('specialnews', u"专题"), 
	('medianewsalbum', u"自媒体图集"), 	
	('ykvideo', u"优酷视频"), 	
)

POSTS_CHOICES = ( 
    ('cheyou' , u"帖子"), 
    ('talk' , u"话题"),
)
TIME_CHOICES = ( 
    (60, u"按分钟"),
    (3600 , u"按小时"),
	(86400 , u"按天"),  

) 
 
FIELD_CHOICES = ( 
    ('posts' , u"发帖"), 
    ('replies' , u"回帖"),         
    ('likes', u"点赞"),
	('attentions', u"关注"),
	('votes', u"投票"),    
) 
POST_CHOICES = ( 
    (99 , u"全部"), 
    (0 , u"普通帖"),         
    (1, u"活动贴"),
	(2, u"问答帖"),
	(3, u"头条分享帖"), 
	(4, u"投票贴"),
	(5, u"提车作业"),	
	(6, u"口碑帖"),	
)
NEWS_SOURCE_CHOICES = ( 
    ('news_add&com' , u"要闻"), 
    ('media' , u"自媒体"),	
	('live_add&com' , u"直播"),	
)
TP_CHOICES = ( 
    ('total' , u"全部"), 
    ('part' , u"部分"),	
)

OB_CHOICES = ( 
	('add', u"新增"),
	('active' , u"活跃"),
)

TR_CHOICES = ( 
    ('transform' , u"转化"), 
    ('trend' , u"趋势"),	
)
TEST_CHOICES = ( 
    ('t' , u"t检验"),        
    ('anova', u"方差分析"),
	('correlation', u"相关系数"),  
) 
PLATFORM_CHOICES= ( 
    ('ADR' , u"ADR"),        
    ('IOS',  u"IOS"),
) 
PLAT_CHOICES= ( 
    ('ALL' , u"全部"), 
	('ADR' , u"ADR"),	
    ('IOS',  u"IOS"),
) 
TARGET_CHOICES= ( 
    ('pv' , u"pv"),        
    ('uv',  u"uv"),
)
TARGET_CHOICE= (
    ('uv',  u"uv"),
    ('pv' , u"pv"),
)
YEAR_CHOICES= ( 
    ('',u"全部"),   
    ('2015',u"2015年"),        
    ('2016', u"2016年"),
) 
MONTH_CHOICES= ( 
    ('',u"全部"),   
    ('1',u"1月"),        
    ('2',u"2月"),
	('3',u"3月"),        
    ('4',u"4月"),
	('5',u"5月"),        
    ('6',u"6月"),
	('7',u"7月"),        
    ('8',u"8月"),
	('9',u"9月"),        
    ('10',u"10月"),
	('11',u"11月"),        
    ('12',u"12月"),
)
WEEKDAY_CHOICES= ( 
    ('',u"全部"),   
    ('2',u"周一"),        
    ('3',u"周二"),
	('4',u"周三"),        
    ('5',u"周四"),
	('6',u"周五"),        
    ('7',u"周六"),
	('1',u"周日"), 
)	
KEY_CHOICES= ( 
    ('active',"日活"),   
    ('newadd',u"新增"),        
    ('login',u"登录"),
	('headline',u"头条"),        
    ('community',u"社区"),
	('car',u"选车"),        
    ('service',u"服务"),
	('my',u"我的"), 
	('media',u"自媒体"), 
	('news',u"要闻"), 
	('video',u"视频"), 
	('news_all',u"阅读总量"), 
	('carmodel',u"车型综述页"), 
	('live',u"直播"), 
	('videoplay',u"视频播放"), 
	('album',u"图集"), 
	('post',u"帖子浏览"), 
	('loan_ok',u"贷款成功"), 
	('buynewcar',u"买新车"), 
	('phone',u"点击400"), 
	('buycar_ok',u"买新车成功"), 
	('replace_ok',u"替换成功"), 
	('askpriceok',u"询底价成功"), 
	('loan',u"贷款"), 
	('phone_call',u"拨打400"), 
	('askprice',u"询底价"), 
	('replace',u"置换"), 
	('media_account_add',u"新增自媒体账号"), 
	('media_follow',u"新增自媒体关注数"), 
	('register',u"新增注册用户"), 
	('coin_give_uv',u"车币发放用户"), 
	('coin_give_pv',u"车币发放数"), 
	('coin_use_pv',u"车币消耗数"), 
	('coin_use_uv',u"车币消耗用户"), 
	('live_add',u"直播新增数"), 
	('live_comment_add',u"直播新增评论数"), 
	('reply_user',u"回帖用户数"), 
	
)

now=datetime.now()
start_init=now-timedelta(days=7)
end_init  =now-timedelta(days=1)

# 起止日期输入框表单模板
class PushForm(forms.ModelForm): 
	start_date = forms.DateField(label="开始日期",required=True,initial=start_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker'}))
	end_date = forms.DateField(label="截止日期",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker1'}))
	
	class Meta: 
		model = Push 
		fields = ('start_date','end_date',) 
		
class AppActiveForm(forms.ModelForm): 
	start_date = forms.DateField(label="开始日期",required=True,initial=start_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker'}))
	end_date = forms.DateField(label="截止日期",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker1'}))
	date_format = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=CHOICES)
		
	class Meta: 
		model = AppIndex
		fields = ('start_date','end_date','date_format',) 
# 起止日期输入框+日期格式表单模板
class NewsRealForm(forms.Form):
	start_date = forms.DateTimeField(label="开始时间",required=True,initial=end_init.strftime('%Y-%m-%d %H:%M:%S'),widget=forms.DateTimeInput(attrs={'id': 'timepicker'}))
	end_date = forms.DateTimeField(label="截止时间",required=True,initial=now.strftime('%Y-%m-%d %H:%M:%S'),widget=forms.DateTimeInput(attrs={'id': 'timepicker1'}))
	news_type = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=NEWS_CHOICES)
	time_scale = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=TIME_CHOICES)
	newsid = forms.CharField(label="新闻id",required=True,help_text='多个id以逗号分隔')

class DailyStartForm(forms.Form):
	start_date = forms.DateField(label="日期",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker'}))
	daily_name = forms.ChoiceField(label="日报",required=True,widget=forms.Select,choices=DAILY_CHOICES)

	
class PostsRealForm(forms.Form):
	start_date = forms.DateTimeField(label="开始时间",required=True,initial=end_init.strftime('%Y-%m-%d %H:%M:%S'),widget=forms.DateTimeInput(attrs={'id': 'timepicker'}))
	end_date = forms.DateTimeField(label="截止时间",required=True,initial=now.strftime('%Y-%m-%d %H:%M:%S'),widget=forms.DateTimeInput(attrs={'id': 'timepicker1'}))
	posts_type = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=POSTS_CHOICES)
	time_scale = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=TIME_CHOICES)
	newsid = forms.CharField(label="帖子id",required=True,help_text='多个id以逗号分隔')
	

		
class ChannelForm(forms.ModelForm):
	start_date=forms.DateField(label="开始时间",required=True,initial=start_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker'}))
	end_date=forms.DateField(label="截止时间",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker1'}))
	ob_format = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=OB_CHOICES)
	class Meta:
		model=Channel
		fields=('start_date','end_date','ob_format',)

class AppStayForm(forms.ModelForm):
	start_date=forms.DateField(label="开始时间",required=True,initial=start_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker'}))
	end_date=forms.DateField(label="截止时间",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker1'}))
	platform = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=TP_CHOICES)
	class Meta:
		model=AppIndex
		fields=('start_date','end_date','platform',)

	
class AppIndexForm(PushForm):
	key_list = forms.MultipleChoiceField(label='',required=False,widget=forms.SelectMultiple(attrs={'style':'height:45px;width:120px;'}),choices=AppKey.objects.filter(c_key__in=['active','newadd','login']).values_list('c_key','c_desc'))
	target_format = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=TARGET_CHOICE)
	class Meta:
		model=AppIndex
		fields=('start_date','end_date',)

class AppIndexSingleForm(PushForm):
	key_list = forms.ChoiceField(label='',required=False,widget=widgets.Select(attrs={'style':'height:25px;width:120px;'}),choices=AppKey.objects.filter(c_key__in=['headline','community','car','service','my']).values_list('c_key','c_desc'))
	target_format = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=TARGET_CHOICE)
	class Meta:
		model=AppIndex
		fields=('start_date','end_date',)

class LogListForm(forms.Form):
	version =forms.CharField(label="版本号",help_text='必需')
	type_desc=forms.CharField(label="事件名",help_text='必需')
	type_name=forms.ChoiceField(label="type",help_text='必需',widget=forms.Select,choices=TypeSet.objects.values_list('type_name','type_desc'))
	page_name=forms.ChoiceField(label="页面",help_text='必需',widget=forms.Select,choices=PageSet.objects.values_list('page_name','page_desc'))
	column_name=forms.CharField(label="栏目",required=False)
	section_name=forms.CharField(label="段落",required=False)
	view_name=forms.ChoiceField(label="视图",help_text='必需',widget=forms.Select,choices=ViewSet.objects.values_list('view_name','view_desc'))
	object_name=forms.CharField(label="名称",required=False)
	object_id=forms.IntegerField(label="ID",required=False,initial=1234)
		
class NewsDataForm(forms.ModelForm): 
	start_date = forms.DateField(label="开始日期",required=True,initial=start_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker'}))
	end_date = forms.DateField(label="截止日期",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker1'}))
	source_format = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=NEWS_SOURCE_CHOICES)	
	class Meta: 
		model = AppIndex
		fields = ('start_date','end_date','source_format',) 		
class PostDetailForm(forms.ModelForm): 
	start_date = forms.DateField(label="开始日期",required=True,initial=start_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker'}))
	end_date = forms.DateField(label="截止日期",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker1'}))
	post_format = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=POST_CHOICES)
	
	class Meta: 
		model = AppIndex 
		fields = ('start_date','end_date','post_format',) 
		
class CommunityHomeForm(forms.ModelForm): 
	start_date = forms.DateField(label="开始日期",required=True,initial=start_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker'}))
	end_date = forms.DateField(label="截止日期",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker1'}))
	target_format = forms.ChoiceField(label="",required=True,widget=forms.RadioSelect,choices=TARGET_CHOICES)
	
	class Meta: 
		model = AppIndex
		fields = ('start_date','end_date','target_format',) 
		
class HeadlineDetailForm(forms.ModelForm): 
	start_date = forms.DateField(label="开始日期",required=True,initial=start_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker'}))
	end_date = forms.DateField(label="截止日期",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker1'}))
	platform = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=PLAT_CHOICES)
	
	class Meta: 
		model = AppIndex
		fields = ('start_date','end_date','platform',) 	


		
class AppSearchForm(forms.ModelForm): 
	start_date = forms.DateField(label="开始日期",required=True,initial=start_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker','style':'height:30px;'}))
	end_date = forms.DateField(label="截止日期",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker1','style':'height:30px;'}))	
	date_year = forms.ChoiceField(label="年",required=False,widget=forms.Select(attrs={'style':'height:30px;'}),choices=YEAR_CHOICES)
	date_month= forms.ChoiceField(label="月",required=False,widget=forms.Select(attrs={'style':'height:30px;'}),choices=MONTH_CHOICES)
	date_weekday=forms.ChoiceField(label="周",required=False,widget=forms.Select(attrs={'style':'height:30px;'}),choices=WEEKDAY_CHOICES)
	class Meta: 
		model = AppIndex 
		fields = ('start_date','end_date','date_year','date_month','date_weekday',) 		
class DataCompareForm(AppActiveForm): 
	field1 = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=FIELD_CHOICES)
	field2 = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=FIELD_CHOICES)
	#field3 = forms.MultipleChoiceField(label='',required=False,widget=forms.CheckboxSelectMultiple(),choices=TEST_CHOICES)
	field3 = forms.MultipleChoiceField(label='',required=False,widget=forms.SelectMultiple(attrs={'style':'height:20px;width:90px;'}),choices=MONTH_CHOICES)
	# groupby_date = forms.DateField(label="分组日期",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'style':'width:90px;'}))
	class Meta: 
		model = AppIndex 
		fields = ('start_date','end_date','date_format','field1','field2','field3',) 

		
class ModuleUserForm(forms.ModelForm): 
	start_date = forms.DateField(label="开始日期",required=True,initial=start_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker'}))
	end_date = forms.DateField(label="截止日期",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker1'}))
#	date_format = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=CHOICES)
	target_format=forms.ChoiceField(label="",required=True,widget=forms.Select,choices=TARGET_CHOICES)
	class Meta: 
		model = AppIndex
		fields = ('start_date','end_date','target_format',) 



class CommunityConverForm(forms.ModelForm): 
	start_date = forms.DateField(label="开始日期",required=True,initial=start_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker'}))
	end_date = forms.DateField(label="截止日期",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker1'}))
	show_format = forms.ChoiceField(label="",required=True,widget=forms.Select,choices=TR_CHOICES)
	class Meta: 
		model = AppIndex
		fields = ('start_date','end_date','show_format',)		

		


# 单个日期输入框表单模板
class AfterOpenForm(forms.ModelForm): 
	
	create_date = forms.DateField(label="create_date",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker'}))
	
	
	class Meta: 
		model = AfterOpen 
		fields = ('create_date',) 
		

		
class PushSendForm(PushForm): 
	start_date = forms.DateField(label="开始日期",required=True,initial=start_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker'}))
	end_date = forms.DateField(label="截止日期",required=True,initial=end_init.strftime('%Y-%m-%d'),widget=forms.DateInput(attrs={'id': 'datepicker1'}))
	platform=forms.ChoiceField(label="",required=True,widget=forms.RadioSelect,choices=PLATFORM_CHOICES)
	class Meta: 
		model = Push 
		fields = ('start_date','end_date','platform',)

class LoginForm(forms.Form): 
	username = forms.CharField(label="用户名")
	password = forms.CharField(label="密码")
		
		
class RegisterForm(forms.ModelForm):
	username=forms.CharField(label="用户名")
	email=forms.EmailField(label="邮箱")
	password=forms.CharField(label="密码")
	
	class Meta:
		model=User
		fields=('username','email','password',)
		
		
class ForgetPasswordForm(forms.Form):
	username=forms.CharField(label="用户名")
	email=forms.EmailField(label="邮箱")
	

class ResetPasswordForm(forms.Form):
	password=forms.CharField(label="新密码")
	
