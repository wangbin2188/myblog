# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,render_to_response,redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django import forms
from flow.models import Flow,FlowNode,Employee
import json
from datetime import datetime,date,timedelta
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# Create your views here.
class CJsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.strftime('%Y-%m-%d %H:%M:%S')
		elif isinstance(obj, date):
			return obj.strftime('%Y-%m-%d')
		else:
			return json.JSONEncoder.default(self, obj)

class FlowForm(forms.ModelForm):
	CHOICES = (('报销', u"报销"),('补签卡', u"补签卡"),('转正申请', u"转正申请"),)
	flow_type=forms.ChoiceField(label="名称",required=True,widget=forms.Select,choices=CHOICES)
	class Meta: 
		model = Flow 
		fields = ('flow_type','remark',)
		
class FlowNodeForm(forms.ModelForm):
	CHOICES = (('agree', u"同意"),('disagree', u"驳回"),)
	operate=forms.ChoiceField(label="审批",required=True,widget=forms.RadioSelect,choices=CHOICES)
	class Meta: 
		model = FlowNode
		fields = ('operate','remark',)
		
class DemandCreateForm(forms.ModelForm):
	title=forms.CharField(label="标题",required=True)
	start_dt = forms.DateField(label="开始",required=True,widget=forms.DateInput(attrs={'id': 'datepicker'}))
	end_dt = forms.DateField(label="截止",required=True,widget=forms.DateInput(attrs={'id': 'datepicker1'}))
	remark = forms.CharField(required=True,widget=forms.Textarea(attrs={'style':'height:0px;width:0px;'}))
	class Meta: 
		model = Flow 
		fields = ('title','remark','executor','start_dt','end_dt')
		
class DemandUpdateForm(forms.ModelForm):
	start_dt = forms.DateField(label="开始",required=True,widget=forms.DateInput(attrs={'id': 'datepicker'}))
	end_dt = forms.DateField(label="截止",required=True,widget=forms.DateInput(attrs={'id': 'datepicker1'}))
	progress=forms.IntegerField(label="进度",required=True,min_value=0,max_value=100,widget=forms.TextInput(attrs={'type': 'range','min':'0','max':'100'}))
	remark = forms.CharField(required=True,widget=forms.Textarea(attrs={'style':'height:0px;width:0px;'}))
	class Meta: 
		model = Flow 
		fields = ('title','remark','start_dt','end_dt','progress')
		
class DemandDistributeForm(forms.ModelForm):
	
	class Meta: 
		model = Flow 
		fields = ('executor_group',)

class DemandNodeForm(forms.ModelForm):
	CHOICES = (('completed', u"完成"),('forward', u"转发"),)
	operate=forms.ChoiceField(label="审批",required=True,widget=forms.RadioSelect,choices=CHOICES)
	class Meta: 
		model = FlowNode
		fields = ('operate','executor',)
		
def flow_create(request):
	if request.method=='GET':
		form=FlowForm()
		return render(request,'flow_create.html',{'form':form})
	elif request.method=='POST':
		form=FlowForm(request.POST) 
		if form.is_valid():
			flow_type=form.cleaned_data['flow_type']
			remark=form.cleaned_data['remark']
			u=Employee.objects.get(user=request.user)
			obj=Flow(flow_type=flow_type,initiator=u.user,remark=remark,state='start',executor=u.leader)
			obj.save()
			obj_node=FlowNode(operator=u.user,operate='start',remark=remark,flowid=obj,executor=u.leader)
			obj_node.save()
		return redirect('flow_submit')

def flow_approval(request,flow_id):
	if request.method=='GET':
		form=FlowNodeForm()
		flownode_list=FlowNode.objects.filter(flowid__id=flow_id)
		flow=Flow.objects.get(id=flow_id)
		if flow.state in ['start','processing'] and flow.executor==request.user:
			return render(request,'flow_approval.html',{'form':form,'flownode_list':flownode_list,'flow':flow})
		else:
			return render(request,'flow_approval.html',{'flownode_list':flownode_list,'flow':flow})
	elif request.method=='POST':
		form=FlowNodeForm(request.POST) 
		if form.is_valid():
			remark=form.cleaned_data['remark']
			operate=form.cleaned_data['operate']
			u=Employee.objects.get(user=request.user)
			obj=Flow.objects.get(id=flow_id)
			if operate=='disagree':
				obj_node=FlowNode(operator=u.user,operate=operate,remark=remark,flowid=obj,executor=None)
				obj_node.save()
				
				obj.state='stop'
				obj.operator_group.add(request.user)
				obj.executor=None
				obj.save()
				return redirect('flow_waitfor')
				
			elif operate=='agree':
				obj_node=FlowNode(operator=u.user,operate=operate,remark=remark,flowid=obj,executor=u.leader)
				obj_node.save()		
							
				if u.leader.username=='boss':
					obj.state='completed'
					obj.operator_group.add(request.user)
					obj.executor=None
					obj.save()
					return redirect('flow_waitfor')
				obj.state='processing'
				obj.operator_group.add(request.user)
				obj.executor=u.leader
				obj.save()
				return redirect('flow_waitfor')
def flow_submit(request):
	if request.method=='GET':
		form=DemandUpdateForm()
		guide='详细'
		guide2='取消'
		guide3='修改'
		flow_list=Flow.objects.filter(initiator=request.user,state__in=['start','processing'])
		return render(request,'flow_submit.html',{'flow_list':flow_list,'guide':guide,'guide2':guide2,'guide3':guide3,'form':form})
	
def flow_complete(request):
	if request.method=='GET':
		guide='详细'
		guide5='唤醒'
		flow_list=Flow.objects.filter(initiator=request.user,state__in=['completed','stop','cancel'])
		return render(request,'flow_submit.html',{'flow_list':flow_list,'guide':guide,'guide5':guide5})
		
def flow_waitfor(request):
	if request.method=='GET':
		form=DemandDistributeForm()
		guide='审批'
		guide4='分发'
		flow_list=Flow.objects.filter(Q(executor=request.user)|Q(executor_group=request.user)).filter(state__in=['start','processing']).distinct()
		return render(request,'flow_submit.html',{'flow_list':flow_list,'guide':guide,'guide4':guide4,'d_form':form})
	elif request.method=='POST':
		form=DemandDistributeForm(request.POST)
		if form.is_valid():
			executor_group=form.cleaned_data['executor_group']
			obj=Flow.objects.get(id=flow_id)
			obj.executor_group=executor_group
			obj.operator_group.add(request.user)
			obj.save()
			for u in obj.executor_group.all():
				obj_node=FlowNode(operator=request.user,operate='distribute',flowid=obj,executor=u)
				obj_node.save()
			return redirect('flow_waitfor')

		
def flow_processed(request):
	if request.method=='GET':
		guide='详细'
		flow_list=Flow.objects.filter(operator_group=request.user)
		return render(request,'flow_submit.html',{'flow_list':flow_list,'guide':guide})	
	
def flow_stop(request,flow_id):
	if request.method=='GET':
		obj=Flow.objects.get(id=flow_id)
		obj.state='stop'
		obj.executor=None
		obj.save()
		obj_node=FlowNode(operator=request.user,operate='stop',flowid=obj,executor=None)
		obj_node.save()
		return redirect('flow_submit')
		
def demand_wake(request,flow_id):
	if request.method=='GET':
		obj=Flow.objects.get(id=flow_id)
		obj.state='processing'
		obj.progress=50
		obj.executor=request.user
		obj.save()
		obj_node=FlowNode(operator=request.user,operate='wake',flowid=obj,executor=request.user)
		obj_node.save()
		return redirect('flow_complete')
		
def demand_create(request):
	if request.method=='GET':
		form=DemandCreateForm()
		return render(request,'flow_create.html',{'form':form})
	elif request.method=='POST':
		form=DemandCreateForm(request.POST) 
		if form.is_valid():
			title=form.cleaned_data['title']
			remark=form.cleaned_data['remark']
			executor=form.cleaned_data['executor']
			start_dt=form.cleaned_data['start_dt']
			end_dt=form.cleaned_data['end_dt']
			u=Employee.objects.get(user=request.user)
			obj=Flow(flow_type='demand',title=title,initiator=u.user,remark=remark,state='start',executor=executor,start_dt=start_dt,end_dt=end_dt)
			obj.save()
			obj_node=FlowNode(operator=u.user,operate='start',remark=remark,flowid=obj,executor=executor)
			obj_node.save()
		return redirect('flow_submit')
		
def demand_update(request,flow_id):
	if request.method=='GET':
		flow=Flow.objects.get(id=flow_id)
		form=DemandUpdateForm(initial={'title':flow.title,
										'remark':flow.remark,
										'progress':flow.progress,
										'start_dt':flow.start_dt.strftime('%Y-%m-%d'),
										'end_dt':flow.end_dt.strftime('%Y-%m-%d')})
		return render(request,'demand_update.html',{'form':form,'flow':flow})
	elif request.method=='POST':
		form=DemandUpdateForm(request.POST)
		if form.is_valid():
			title=form.cleaned_data['title']
			remark=form.cleaned_data['remark']
			start_dt=form.cleaned_data['start_dt']
			end_dt=form.cleaned_data['end_dt']
			progress=form.cleaned_data['progress']
			obj=Flow.objects.get(id=flow_id)
			obj.title=title
			obj.remark=remark
			obj.start_dt=start_dt
			obj.end_dt=end_dt
			obj.progress=progress
			obj.save()
			obj_node=FlowNode(operator=request.user,operate='update',flowid=obj,executor=obj.executor)
			obj_node.save()
		return redirect('flow_submit')

def demand_approval(request,flow_id):
	if request.method=='GET':
		form=DemandNodeForm()
		flownode_list=FlowNode.objects.filter(flowid__id=flow_id)
		flow=Flow.objects.get(id=flow_id)
		if flow.state in ['start','processing'] and flow.executor==request.user:
			return render(request,'flow_approval.html',{'form':form,'flownode_list':flownode_list,'flow':flow})
		else:
			return render(request,'flow_approval.html',{'flownode_list':flownode_list,'flow':flow})
	elif request.method=='POST':
		form=DemandNodeForm(request.POST) 
		if form.is_valid():
			operate=form.cleaned_data['operate']
			executor=form.cleaned_data['executor']
			u=Employee.objects.get(user=request.user)
			obj=Flow.objects.get(id=flow_id)
			if operate=='completed':
				obj_node=FlowNode(operator=u.user,operate=operate,flowid=obj,executor=None)
				obj_node.save()
				
				obj.state='completed'
				obj.operator_group.add(request.user)
				obj.progress=100
				obj.executor=None
				obj.save()
				return redirect('flow_waitfor')
				
			elif operate=='forward':
				obj_node=FlowNode(operator=u.user,operate=operate,flowid=obj,executor=executor)
				obj_node.save()
				
				obj.state='processing'
				obj.operator_group.add(request.user)
				obj.progress=30
				obj.executor=executor
				obj.save()
				return redirect('flow_waitfor')
				

def flow_add(request):
	return render(request,'flow_add.html',{})
	
import datetime
import time
def time2stamp(c_time):
	timestamp=time.mktime(c_time.timetuple())
	return  int(timestamp)*1000
	
def demand_chart(request):
	if request.method=='GET':
		guide='审批'
		flow_list=Flow.objects.filter(executor=request.user,state__in=['start','processing'],flow_type='demand')
		label=[]
		s_dt=[]
		e_dt=[]
		for item in flow_list:
			label.append(item.title)
			s_dt.append(time2stamp(item.start_dt))
			e_dt.append(time2stamp(item.end_dt))
		
		return render(request,'demand_chart.html',{'flow_list':flow_list,'label':json.dumps(label),'s_dt':json.dumps(s_dt),'e_dt':json.dumps(e_dt)})

def demand_distribute(request,flow_id):
	if request.method=='GET':
		flow=Flow.objects.get(id=flow_id)
		form=DemandDistributeForm(initial={'start_dt':flow.start_dt.strftime('%Y-%m-%d'),'end_dt':flow.end_dt.strftime('%Y-%m-%d'),'remark':flow.remark})
		return render(request,'demand_distribute.html',{'form':form,'flow':flow})
	elif request.method=='POST':
		form=DemandDistributeForm(request.POST)
		if form.is_valid():
			executor_group=form.cleaned_data['executor_group']
			obj=Flow.objects.get(id=flow_id)
			obj.executor_group=executor_group
			obj.operator_group.add(request.user)
			obj.save()
			for u in obj.executor_group.all():
				obj_node=FlowNode(operator=request.user,operate='distribute',flowid=obj,executor=u)
				obj_node.save()
		return redirect('flow_waitfor')	

