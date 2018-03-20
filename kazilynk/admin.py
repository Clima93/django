from django.contrib import admin
from accounts.models import UserAccount, WorkIndustry, Industry, WorkExperience, Institute, Job, Service

class AccountAdmin(admin.ModelAdmin):
	list_display = ['user','email', 'first_name', 'last_name', 'category', 'created_on']
	exclude = ['user', 'email_validation_expire', 'email_verification_code', 'created_on', 'services', 'industry']
	list_filter = ['category']

	def email(self, obj):
		return obj.user.email

	email.short_description = "Email"
	email.admin_order_field = 'email'

class WorkIndustryAdmin(admin.ModelAdmin):
	list_display = ['name', 'active', 'start_time']
	list_filter = ['active']

class JobAdmin(admin.ModelAdmin):
	list_display = ['job_title', 'start_date', 'end_date', 'check_status']

admin.site.register(UserAccount, AccountAdmin)
admin.site.register(WorkIndustry, WorkIndustryAdmin)
admin.site.register(Industry)
admin.site.register(WorkExperience)
admin.site.register(Institute)
admin.site.register(Job, JobAdmin)
admin.site.register(Service)