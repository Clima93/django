"""kazilynk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from accounts import views
from django.conf import settings
from django.views.generic import TemplateView
from kazilynk import views
from accounts import urls
from django.core.urlresolvers import reverse

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/profile$', views.profile, name="profile_page"),
    url(r'^accounts/profile/$', views.profile, name="profile_page_slash"),
    url(r'^accounts/employer$', views.employer_page, name="employer_page"),
    url(r'^accounts/service-provider$', views.service_provider_page, name="service_provider"),
    # url(r'^accounts/service-seeker$', views.service_seeker_page, name="service_seeker"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^lynkspiration/$', views.lynkspiration, name="lynkspiration"),
    url(r'^job/(?P<job_id>\d+)$', views.view_job, name="view_job"),
    # url(r'^service/(?P<service_id>\d+)$', views.view_service, name='view_service'),
    # url(r'^edit-service/(?P<service_id>\d+)$', views.edit_service, name="edit_service"),
    url(r'^delete-job/(?P<job_id>\d+)$', views.delete_job, name="delete_job"),
    # url(r'^delete-service/(?P<service_id>\d+)$', views.delete_service, name="delete_service"),
    # url(r'^view-profile/(?P<user_id>\d+)$', views.view_profile, name="view_profile"),
    url(r'^article/(?P<slug>.+)$', views.view_article, name="view_article"),
    url(r'^add-service$', views.add_service, name="add_service"),
    url(r'^add-service$', views.add_service, name="add_service"),
    url(r'^check-post-cv/$', views.check_post_cv, name="check_post_cv"),
    url(r'^check_post_job/$', views.check_post_job, name="check_post_job"),
    url(r'^check_post_service$', views.check_post_service, name="check_post_service"),
    url(r'^change-user-type$', views.change_user_type, name="change-user-type"),
    # url(r'^contact-provider/(?P<service_id>\d+)$', views.contact_provider, name="contact_provider"),
    # url(r'^signup-newsletter$', "accounts.views.signup_newsletter"),
    url(r'^update-user-type$', views.update_user_type, name="update_user_type"),
    url(r'^update-user-type$', "accounts.views.update_service"),
    url(r'^edit-job$', "accounts.views.edit_job_ajax"),
    url(r'^delete-job$', "accounts.views.delete_job_ajax"),
    url(r'^delete-service$', "accounts.views.delete_service_ajax"),
    url(r'^service-post$', "accounts.views.service_post"),
    url(r'^service-update$', "accounts.views.service_update"),
    url(r'^search-ajax$', "accounts.views.search_ajax"),
    url(r'^contact-send$', "accounts.views.contact_send"),
    url(r'^search$', views.search, name="search"),
    url(r'^register$', "accounts.views.register"),
    url(r'^test$', views.job_list, name="job_list"),
    url(r'^register/', include('accounts.urls')),
    url(r'^$', views.home),
    url(r'^index$', views.home),
    url(r'^employers$', TemplateView.as_view(template_name="employers.html"), name="employer_info"),
    url(r'^job-seekers$', TemplateView.as_view(template_name="job-seekers.html"), name="job_seeker"),
    url(r'^privacy$', TemplateView.as_view(template_name="privacy.html"), name="privacy"),
    url(r'^about-us$', TemplateView.as_view(template_name="about-us.html"), name="about_us"),
    url(r'^terms-and-conditions$', TemplateView.as_view(template_name="terms_conditions.html"), name="terms"),
    url(r'^pricing-policy$', TemplateView.as_view(template_name="pricing.html"), name="pricing"),
    url(r'^contact-us$', TemplateView.as_view(template_name="contact.html"), name="contact"),

]
