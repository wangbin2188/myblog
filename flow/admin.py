from django.contrib import admin
from flow.models import Employee

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
	list_display=('user','leader',)

admin.site.register(Employee,EmployeeAdmin)
