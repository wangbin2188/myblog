# -*- coding: UTF-8 -*-
from pyquery import PyQuery as pq
import re
from datetime import datetime,timedelta
import pymysql
import logging
from bs4 import BeautifulSoup
import requests
import urllib
import urllib2
import json
import codecs
from sqlalchemy import Column, String, create_engine,Integer,Date,Numeric,Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 


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
		
Base = declarative_base()

class AppIndex(Base):

	__tablename__ = 'push_appindex'
	
	id=Column(Integer,primary_key=True)
	dt=Column(Date)
	c_key = Column(String(30))
	c_value = Column(Text)
	
def community_detail(key,start_date,end_date):
	url = 'http://api.ycapp.yiche.com/Statistics/GetStatisValByMetas'
	user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
	referer='http://baa.bitauto.com/lady/index-68-all-2-0.html'
	headers={'User-Agent':user_agent,'Referer':referer}
	values={}
	values['metas']=key
	values['start']=start_date
	values['end']=end_date
	data = urllib.urlencode(values) 
	geturl = url + "?"+data
	request = urllib2.Request(geturl,headers=headers)
	response = urllib2.urlopen(request)
	js=json.loads(response.read())
	return js
	
def community_home(key,start_date,end_date):
	url = 'http://api.ycapp.yiche.com/Statistics/GetStatisValByMetas'
	user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
	referer='http://baa.bitauto.com/lady/index-68-all-2-0.html'
	headers={'User-Agent':user_agent,'Referer':referer}
	values={}
	values['metas']=key
	values['start']=start_date
	values['end']=end_date
	data = urllib.urlencode(values) 
	geturl = url + "?"+data
	request = urllib2.Request(geturl,headers=headers)
	response = urllib2.urlopen(request)
	js=json.loads(response.read())
	try:
		return js['data'][key][0]
	except IndexError,e:
		return {'val':0}
	
	
def insert_postdetail(start_date,end_date):
	while start_date<end_date:
		print start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d')		
		result=community_detail('AdminDailyStats',start_date.strftime('%Y-%m-%d'),start_date.strftime('%Y-%m-%d'))
		data= result['data']['AdminDailyStats']
		for items in data:
			s_year,s_month,s_day=items['date'].split('-')
			start_date=datetime(int(s_year),int(s_month),int(s_day))
			week_start=start_date-timedelta(start_date.weekday())
			week_end=week_start+timedelta(days=6)
			week=week_start.strftime('%m/%d')+'~'+week_end.strftime('%m/%d')	
			month=start_date.strftime('%Y/%m')
			value=json.loads(items['val'])
			cheyou=value['CheYouDetails']
			detail_list= [dict(DailyTopicAdd=item.get('DailyTopicAdd',0),
							AppDailyTopicAdd=item.get('AppDailyTopicAdd',0),
							AppDailyTopicUv=item.get('AppDailyTopicUv',0),
							AppDailyReplyAdd=item.get('AppDailyReplyAdd',0),
							AppDailyReplyAddUv=item.get('AppDailyReplyAddUv',0),
							DailyLikeCount=item.get('DailyLikeCount',0),							
							AppDailyGoodTopicCount=item.get('AppDailyGoodTopicCount',0),							
							DailyHomeCount=item.get('DailyHomeCount',0),
							TopicMode=item.get('TopicMode',0) ) for item in cheyou ]			
			print detail_list
			all_list= [dict(DailyTopicAdd=value.get('DailyTopicAdd',0),
							AppDailyTopicAdd=value.get('AppDailyTopicAdd',0),
							AppDailyTopicUv=value.get('AppDailyTopicUv',0),
							AppDailyReplyAdd=value.get('AppDailyReplyAdd',0),
							AppDailyReplyAddUv=value.get('AppDailyReplyAddUv',0),
							DailyLikeCount=value.get('DailyLikeCount',0),							
							AppDailyGoodTopicCount=value.get('AppDailyGoodTopicCount',0),							
							DailyHomeCount=value.get('DailyHomeCount',0),
							TopicMode=99 )  ]
			print all_list
			session.bulk_insert_mappings(AppIndex,[dict(dt=start_date.strftime('%Y-%m-%d'),c_key='all_posts',c_value=json.dumps(item)) for item in all_list])
			session.bulk_insert_mappings(AppIndex,[dict(dt=start_date.strftime('%Y-%m-%d'),c_key=topic2mode(item['TopicMode']),c_value=json.dumps(item)) for item in detail_list])
			start_date=start_date+timedelta(days=1)

def insert_media(start_date,end_date):
	while start_date<end_date:
		media=community_detail('AdminMediaData',start_date,start_date)['data']['AdminMediaData'][0]['val']
		print media
		session.bulk_insert_mappings(AppIndex,[dict(dt=start_date.strftime('%Y-%m-%d'),c_key='media',c_value=media)])
		start_date=start_date+timedelta(days=1)

def insert_postsadd(start_date,end_date):
	while start_date<end_date:	
		result=community_detail('AdminDailyStats',start_date.strftime('%Y-%m-%d'),start_date.strftime('%Y-%m-%d'))
		data= result['data']['AdminDailyStats']
		for items in data:
			week_start=start_date-timedelta(start_date.weekday())
			week_end=week_start+timedelta(days=6)
			week=week_start.strftime('%m/%d')+'~'+week_end.strftime('%m/%d')	
			month=start_date.strftime('%Y/%m')
			value=json.loads(items['val'])
			cheyou=value['CheYouDetails']
			post_dict={}
			for item in  cheyou:
				if item['TopicMode']==0:
					post_dict['topic_posts']=item.get('AppDailyTopicAdd',0)
				elif item['TopicMode']==1:
					post_dict['activity_posts']=item.get('AppDailyTopicAdd',0)
				elif item['TopicMode']==2:
					post_dict['question_posts']=item.get('AppDailyTopicAdd',0)
				elif item['TopicMode']==3:
					post_dict['share_posts']=item.get('AppDailyTopicAdd',0)
				elif item['TopicMode']==4:
					post_dict['vote_posts']=item.get('AppDailyTopicAdd',0)
				elif item['TopicMode']==5:
					post_dict['bycar_posts']=item.get('AppDailyTopicAdd',0)
				elif item['TopicMode']==6:
					post_dict['koubei_posts']=item.get('AppDailyTopicAdd',0)
			post_list=[dict(topic_posts=post_dict.get('topic_posts',0),
							activity_posts=post_dict.get('activity_posts',0),
							question_posts=post_dict.get('question_posts',0),
							vote_posts=post_dict.get('vote_posts',0),
							bycar_posts=post_dict.get('bycar_posts',0),
							share_posts=post_dict.get('share_posts',0),
							koubei_posts=post_dict.get('koubei_posts',0))]
			session.bulk_insert_mappings(AppIndex,[dict(dt=start_date.strftime('%Y-%m-%d'),c_key='posts_add',c_value=json.dumps(item)) for item in post_list])
			print post_list
			start_date=start_date+timedelta(days=1)
		
def insert_module(start_date,end_date):
	headline_key='TouTiaoUserViewCount'
	community_key=['hd-shequ-tab-click-device_ios','shequ-tab-click-device_ios','shequ-tab-click-device_android']
	selectcar_key=['car-tab-click-device_android','car-tab-click-device_ios','hd-car-tab-click-device_ios']
	service_key=['YC-Tab-device_android','YC-Tab-device_ios','hd-YC-Tab-device_ios']
	my_key=['my-tab-click-device_ios','hd-my-tab-click-device_ios','my-tab-click-device_android']
	headline_pv_key=['hd-toutiao-tab-click_ios','toutiao-tab-click_ios','toutiao-tab-click_android']
	community_pv_key=['hd-shequ-tab-click_ios','shequ-tab-click_ios','shequ-tab-click_android']
	selectcar_pv_key=['car-tab-click_android','car-tab-click_ios','hd-car-tab-click_ios']
	service_pv_key=['YC-Tab_android','YC-Tab_ios','hd-YC-Tab_ios']
	my_pv_key=['my-tab-click_ios','hd-my-tab-click_ios','my-tab-click_android']
	while start_date<end_date:
		headline_user= community_home(headline_key,start_date,start_date)['val']
		community_user=int(community_home(community_key[0],start_date,start_date)['val'])+int(community_home(community_key[1],start_date,start_date)['val'])+int(community_home(community_key[2],start_date,start_date)['val'])
		selectcar_user=int(community_home(selectcar_key[0],start_date,start_date)['val'])+int(community_home(selectcar_key[1],start_date,start_date)['val'])+int(community_home(selectcar_key[2],start_date,start_date)['val'])
		service_user=int(community_home(service_key[0],start_date,start_date)['val'])+int(community_home(service_key[1],start_date,start_date)['val'])+int(community_home(service_key[2],start_date,start_date)['val'])
		my_user=int(community_home(my_key[0],start_date,start_date)['val'])+int(community_home(my_key[1],start_date,start_date)['val'])+int(community_home(my_key[2],start_date,start_date)['val'])
		uv_list=[dict(headline=headline_user,
					community=community_user,
					car=selectcar_user,
					service=service_user,
					my=my_user)]
		print uv_list
		session.bulk_insert_mappings(AppIndex,[dict(dt=start_date.strftime('%Y-%m-%d'),c_key='module_uv',c_value=json.dumps(item)) for item in uv_list])
		headline_pv= int(community_home(headline_pv_key[0],start_date,start_date)['val'])+int(community_home(headline_pv_key[1],start_date,start_date)['val'])+int(community_home(headline_pv_key[2],start_date,start_date)['val'])
		community_pv=int(community_home(community_pv_key[0],start_date,start_date)['val'])+int(community_home(community_pv_key[1],start_date,start_date)['val'])+int(community_home(community_pv_key[2],start_date,start_date)['val'])
		selectcar_pv=int(community_home(selectcar_pv_key[0],start_date,start_date)['val'])+int(community_home(selectcar_pv_key[1],start_date,start_date)['val'])+int(community_home(selectcar_pv_key[2],start_date,start_date)['val'])
		service_pv=int(community_home(service_pv_key[0],start_date,start_date)['val'])+int(community_home(service_pv_key[1],start_date,start_date)['val'])+int(community_home(service_pv_key[2],start_date,start_date)['val'])
		my_pv=int(community_home(my_pv_key[0],start_date,start_date)['val'])+int(community_home(my_pv_key[1],start_date,start_date)['val'])+int(community_home(my_pv_key[2],start_date,start_date)['val'])
		pv_list=[dict(headline=headline_pv,
					community=community_pv,
					car=selectcar_pv,
					service=service_pv,
					my=my_pv)] 
		print pv_list
		session.bulk_insert_mappings(AppIndex,[dict(dt=start_date.strftime('%Y-%m-%d'),c_key='module_pv',c_value=json.dumps(item)) for item in pv_list])
		start_date=start_date+timedelta(days=1)

def insert_appstay(start_date,end_date):
	app_stay_key='TabResidenceTime'
	while start_date<end_date:
		stay_val= community_home(app_stay_key,start_date,start_date)['val']
		session.bulk_insert_mappings(AppIndex,[dict(dt=start_date.strftime('%Y-%m-%d'),c_key='appstay',c_value=stay_val)])
		print stay_val
		start_date=start_date+timedelta(days=1)

def insert_news(start_date,end_date):
	while start_date<end_date:
		important_result=community_detail('AdminDailyStats',start_date.strftime('%Y-%m-%d'),start_date.strftime('%Y-%m-%d'))['data']['AdminDailyStats'][0]['val']
		important_result=json.loads(important_result)
		important_list=[dict(DailyNewsAdd=important_result['DailyNewsAdd'],DailyCommentAdd=important_result['DailyCommentAdd'])]
		print important_list
		session.bulk_insert_mappings(AppIndex,[dict(dt=start_date.strftime('%Y-%m-%d'),c_key='news_add&com',c_value=json.dumps(item)) for item in important_list])
		start_date=start_date+timedelta(days=1)
	
def insert_appvideo(start_date,end_date):
	adrvideo_key='AndroidVideoPlayCount'
	iosvideo_key='IOSVideoPlayCount'
	while start_date<end_date:
		adr_data= community_home(adrvideo_key,start_date,start_date)['val']
		ios_data= community_home(iosvideo_key,start_date,start_date)['val']
		temp_list=[dict(adr_video=adr_data,ios_video=ios_data)] 
		print temp_list
		session.bulk_insert_mappings(AppIndex,[dict(dt=start_date.strftime('%Y-%m-%d'),c_key='server_videoplay',c_value=json.dumps(item)) for item in temp_list])
		start_date=start_date+timedelta(days=1)

def insert_live(start_date,end_date):
	live_add_key='s_dayapp_liveadd_count'
	live_comment_key='s_dayapp_livecommentadd_count'
	while start_date<end_date:
		try:
			live_add_data=community_detail(live_add_key,start_date,start_date)['data'][live_add_key][0]['val']
		except IndexError:
			live_add_data=0
		try:
			live_comment_data=community_detail(live_comment_key,start_date,start_date)['data'][live_comment_key][0]['val']
		except IndexError:
			live_comment_data=0
		temp_list=[dict(live_add=live_add_data,live_comment=live_comment_data)]
		print temp_list
		session.bulk_insert_mappings(AppIndex,[dict(dt=start_date.strftime('%Y-%m-%d'),c_key='live_add&com',c_value=json.dumps(item)) for item in temp_list])
		start_date=start_date+timedelta(days=1)	


def insert_coindata(start_date,end_date):
	while start_date<end_date:
		coin_give_uv=community_detail('s_dayapp_fafangchebiuser_count',start_date,start_date)['data']['s_dayapp_fafangchebiuser_count'][0]['val']
		coin_give_pv=community_detail('s_dayapp_fafangchebi_count',start_date,start_date)['data']['s_dayapp_fafangchebi_count'][0]['val']
		coin_use_pv=community_detail('s_dayapp_xiaohaochebi_count',start_date,start_date)['data']['s_dayapp_xiaohaochebi_count'][0]['val']
		coin_use_uv=community_detail('s_dayapp_xiaohaochebiuser_count',start_date,start_date)['data']['s_dayapp_xiaohaochebiuser_count'][0]['val']
		value_list= [dict(give_uv=coin_give_uv,give_pv=coin_give_pv,use_pv=abs(int(coin_use_pv)),use_uv=coin_use_uv)]
		session.bulk_insert_mappings(AppIndex,[dict(dt=start_date.strftime('%Y-%m-%d'),c_key='car_coin',c_value=json.dumps(item)) for item in value_list])
		print value_list
		start_date=start_date+timedelta(days=1)

def insert_evaluation(start_date,end_date):
	while start_date<end_date:
		evaluation_add=community_detail('s_dayapp_koubeitopicadd_count',start_date,start_date)['data']['s_dayapp_koubeitopicadd_count'][0]['val']
		evaluation_comment=community_detail('s_dayapp_koubeitopiccomment_count',start_date,start_date)['data']['s_dayapp_koubeitopiccomment_count'][0]['val']
		evaluation_add_uv=community_detail('s_dayapp_koubeitopicuser_count',start_date,start_date)['data']['s_dayapp_koubeitopicuser_count'][0]['val']
		evaluation_comment_uv=community_detail('s_dayapp_koubeitopicreplyuser_count',start_date,start_date)['data']['s_dayapp_koubeitopicreplyuser_count'][0]['val']
		value_list= [dict(evaluation_add=evaluation_add,evaluation_comment=evaluation_comment,evaluation_add_uv=evaluation_add_uv,evaluation_comment_uv=evaluation_comment_uv)]
		session.bulk_insert_mappings(AppIndex,[dict(dt=start_date.strftime('%Y-%m-%d'),c_key='car_evaluation',c_value=json.dumps(item)) for item in value_list])
		print value_list
		start_date=start_date+timedelta(days=1)	
	
	
if __name__=='__main__':
	s_date=sys.argv[1]
	e_date=sys.argv[2]
	s_year,s_month,s_day=s_date.split('-')
	e_year,e_month,e_day=e_date.split('-')
	start_date=datetime(int(s_year),int(s_month),int(s_day))
	end_date=datetime(int(e_year),int(e_month),int(e_day))
	engine = create_engine('mysql://root:wangbin@localhost:3306/chart')
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	insert_postdetail(start_date,end_date)
	insert_media(start_date,end_date)
	insert_postsadd(start_date,end_date)
	insert_module(start_date,end_date)
	insert_appstay(start_date,end_date)
	insert_news(start_date,end_date)
	insert_live(start_date,end_date)
	insert_appvideo(start_date,end_date)
	insert_coindata(start_date,end_date)
	insert_evaluation(start_date,end_date)
	session.commit()
	session.close()


# register=community_detail('s_dayapp_registeruser_count',start_date,start_date)['data']['s_dayapp_registeruser_count'][0]['val']
# result=community_detail('AdminDailyStats',start_date.strftime('%Y-%m-%d'),start_date.strftime('%Y-%m-%d'))['data']['AdminDailyStats'][0]['val']
# result=json.loads(result)
# follow_add=result['AppDailyFollowCount']
# value2=[start_date.strftime('%Y-%m-%d'),'follow_add',follow_add,'pv']
