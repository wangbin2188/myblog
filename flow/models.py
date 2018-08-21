# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
#from DjangoUeditor.models import UEditorField
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your models here.

class Employee(models.Model):
	user=models.ForeignKey(User,verbose_name='用户名',related_name='user_name')
	leader=models.ForeignKey(User,verbose_name='直接领导',related_name='leader_name')
	
		
class Flow(models.Model):
	flow_type = models.CharField(max_length = 20,verbose_name = '流名称')
	title=models.CharField(max_length = 40,verbose_name = '标题',default='')
	create_dt = models.DateTimeField(auto_now_add = True,verbose_name = '创建时间')
	update_dt = models.DateTimeField(auto_now = True,verbose_name = '更新时间')
	initiator = models.ForeignKey(User,verbose_name = '发起人',related_name = 'partner_name')
	remark = models.TextField(null = True,verbose_name = '发起内容')
	state = models.CharField(max_length = 20,verbose_name = '流状态')
	executor = models.ForeignKey(User,verbose_name = '指派给',null = True, on_delete = models.SET_NULL,related_name = 'executor')
	start_dt = models.DateField(null = True,blank = True,verbose_name = '任务开始')
	end_dt = models.DateField(null = True,blank = True,verbose_name = '任务完成')
	progress= models.IntegerField(null = True,blank = True,default=0,verbose_name = '进度')
	executor_group = models.ManyToManyField(User,verbose_name = '分配给',null = True,related_name = 'executor_group')
	operator_group = models.ManyToManyField(User,verbose_name = '经手人',null = True,related_name = 'operator_group')
	def get_absolute_url(self):
		if self.flow_type=='demand':
			return reverse('demand_approval',args=(self.id,))
		return reverse('flow_approval',args=(self.id,))
	

class FlowNode(models.Model):
	operator=models.ForeignKey(User,verbose_name='操作者',related_name='operator')
	c_dt=models.DateTimeField(auto_now=True,verbose_name='触发时间')
	operate=models.CharField(max_length=20,verbose_name='操作')
	remark=models.TextField(null=True,verbose_name='备注内容')
	flowid=models.ForeignKey(Flow,verbose_name='工作流ID')
	executor=models.ForeignKey(User,verbose_name='指派给',null=True, on_delete=models.SET_NULL,related_name='operator_name')
	
		
	class Meta:
		ordering=['c_dt']
