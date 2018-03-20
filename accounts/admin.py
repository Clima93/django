from django.contrib import admin
from accounts.models import UserAccount, WorkIndustry, Industry, WorkExperience, Institute, Job, Service, UserService
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from django.conf import settings
from_email = settings.EMAIL_HOST_USER
from django.http import HttpResponse

def send_email(modeladmin, request, queryset):
	context = {'queryset': queryset}
	body = render_to_string('snippets/user-data.txt', context)

	msg = EmailMessage('Kazilynk: message from contact us form', body, from_email, [request.user.email])
	msg.send()

send_email.short_description = "Send to email"

def download_info(modeladmin, request, queryset):
	context = {'queryset': queryset}
	body = render_to_string('snippets/user-data.txt', context)

	txtfile = open('django_project/media/user-info.txt', 'w')
	txtfile.write(body)
	txtfile.close()

	f = open('django_project/media/user-info.txt', 'r')

	response = HttpResponse(f, content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=data.txt'
	return response

download_info.short_description = "Download info"

class AccountAdmin(admin.ModelAdmin):
	list_display = ['user','email', 'first_name', 'last_name', 'category', 'created_on']
	exclude = ['user', 'email_validation_expire', 'email_verification_code', 'created_on', 'services', 'industry']
	list_filter = ['category']
	actions=[download_info, send_email]

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
admin.site.register(UserService)