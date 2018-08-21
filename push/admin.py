# -*- coding: UTF-8 -*-
from django.contrib import admin
from django import forms
from push.models import AppBusiness,AppDaily,AppChart,TypeSet,PageSet,ViewSet,ObjectSet,LogList,AppVersion
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import urlparse
from django.shortcuts import redirect
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class AppBusinessAdmin(admin.ModelAdmin):
	list_display=('yipai','yixin','huimaiche','yichehui','ershouche','date',)
	search_fields=('date',)
	list_filter=('date',)
admin.site.register(AppBusiness,AppBusinessAdmin)

class AppDailyAdmin(admin.ModelAdmin):
	list_display=('daily_key','daily_desc',)

class AppChartAdmin(admin.ModelAdmin):
	list_display=('chart_key','chart_desc','chart_list','chart_column',)

class TypeSetAdmin(admin.ModelAdmin):
	list_display=('type_name','type_desc',)

class PageSetAdmin(admin.ModelAdmin):
	list_display=('module_name','page_name','page_desc',)

class ViewSetAdmin(admin.ModelAdmin):
	list_display=('view_name','view_desc',)
class ObjectSetAdmin(admin.ModelAdmin):
	list_display=('object_name','object_desc',)
	
#class LogListForm(forms.ModelForm):
#	def clean(self):
#		cleaned_data = super(LogListForm,self).clean()
#		object_type = cleaned_data['object_type']
#		object_name = cleaned_data['object_name']
#		if object_type=='other' and object_name is null:
#			raise forms.ValidationError('若对象为其他,则Name不可为空')
#		return cleaned_data
#			
#	class Meta:
#		model = LogList
#		fields = '__all__'

class LogListAdmin(admin.ModelAdmin):
#	form = LogListForm
	exclude =('dt','user_name','object_id',)
	list_display=('version','user_name','type_desc','type_name','page_name','view_name','section_name','object_name',)
	list_display_links =('type_desc',)
	search_fields=('version',)
	list_filter=('version','user_name__first_name',)
	save_on_top=True
	#list_editable=('user_name','type_desc','type_name','page_name','view_name','dt','object_name',)
	#def formfield_for_foreignkey(self, db_field, request, **kwargs):
	#	if db_field.name == "user_name":
	#		kwargs["queryset"] =User.objects.filter(username=request.user.username)
	#	return super(LogListAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def save_model(self, request, obj, form, change):
		cleaned_data=form.clean()
		object_type= cleaned_data.get("object_type")
		object_name= cleaned_data.get("object_name")
		if object_type.object_name!='other':
			obj.object_id=1234
		elif object_type.object_name=='other':
			obj.object_id=None
		obj.user_name = request.user
		obj.save()

	def download(self,request,queryset):
		selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
		url = urlparse.urljoin('/push/log_export/','%s/'%(",".join(selected)))
		return redirect(url)
	actions = [download]

admin.site.register(AppDaily,AppDailyAdmin)
admin.site.register(AppChart,AppChartAdmin)
admin.site.register(TypeSet,TypeSetAdmin)
admin.site.register(PageSet,PageSetAdmin)
admin.site.register(ViewSet,ViewSetAdmin)
admin.site.register(ObjectSet,ObjectSetAdmin)
admin.site.register(LogList,LogListAdmin)
admin.site.register(AppVersion)
# Register your models here.
