from django.contrib import admin
from common.models import Location, Quote, Article, ServiceAlert, NewsLetterEmail

class LocationAdmin(admin.ModelAdmin):
	search_fields = ['name', 'country_name', 'country_code']

class ArticleAdmin(admin.ModelAdmin):
	list_display = ['title', 'active', 'on_homepage', 'popular', 'top_article']
	list_filter = ['on_homepage', 'popular', 'top_article']

admin.site.register(Location, LocationAdmin)
admin.site.register(Quote)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ServiceAlert)
admin.site.register(NewsLetterEmail)