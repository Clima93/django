from django.conf.urls import include, url, patterns
from django.views.generic import TemplateView
from accounts.views import service_provider, my_jobs_view, update_job, update_employer, application_questions, employer_page, update_social, social_links, update_documents, documents, update_language, language, update_skill, skills, education_form, update_education, education, update_work_experience, work_experience, update_job_criteria, job_criteria, update_user_profile, profile_userdetails, update_category, socialauth, signup, email_checkup_json, create_user, complete, confirm_verification, update_profile, user_details, deactivate_industry, activate_industry

from django.contrib.auth.views import password_change, password_change_done, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from accounts.views import JobListView
from django.views.generic import ListView

urlpatterns = [
    url(r'^signup$', signup),
    url(r'^service-provider$', service_provider),
    url(r'^profile_home$', profile_userdetails, name="profile_details"),
    url(r'^job_criteria$', job_criteria, name="job_criteria"),
    url(r'^work_experience$', work_experience, name="work_experience"),
    url(r'^education$', education, name="education"),
    url(r'^skills$', skills, name="skills"),
    url(r'^language$', language, name="language"),
    url(r'^documents$', documents, name="documents"),
    url(r'^social-links$', social_links, name="social_links"),
    url(r'^application-questions$', application_questions, name="application_questions"),
    url(r'^post-job$', update_job, name="post_job"),
    url(r'^create-job$',my_jobs_view, name="create_job"),
    url(r'^complete_signup$', socialauth),
    url(r'^create_user$', create_user),
    url(r'^complete$', complete),
    url(r'^check_email$', email_checkup_json),
    url(r'^update_profile$', update_profile),
    url(r'^update_employer$', update_employer),
    url(r'^update_employer_2$', update_job),
    url(r'^update_user_profile$', update_user_profile),
    url(r'^update_job_criteria$', update_job_criteria),
    url(r'^update_work_experience$', update_work_experience),
    url(r'^update_education$', update_education),
    url(r'^update_skill$', update_skill),
    url(r'^update_language$', update_language),
    url(r'^update_documents$', update_documents),
    url(r'^unlink_social$', update_social),
    url(r'^update_category$', update_category),
    url(r'^user-details$', user_details, name="user_details"),
    url(r'^account_completion/(?P<user_id>\d+)/(?P<code>[-\w]+)$', confirm_verification, name="confirmation_link"),
    url(r'^industry-demote/(?P<work_id>\d+)/(?P<code>[-\w]+)$', deactivate_industry, name="deactivate_industry"),
    url(r'^industry-activate/(?P<work_id>\d+)/(?P<code>[-\w]+)$', activate_industry, name="activate_industry"),
    url(r'^work_experience_form$', TemplateView.as_view(template_name="snippets/work_experience_form.html")),
    url(r'^education_form$', education_form),
    url(r'^language_form$', TemplateView.as_view(template_name="snippets/language_form.html")),
    url(r'^link_form$', TemplateView.as_view(template_name="snippets/link_form.html")),
    url(r'^document_form$', TemplateView.as_view(template_name="snippets/document_form.html")),
    url(r'^price_form$', TemplateView.as_view(template_name="snippets/price_form.html")),
    url(r'^', JobListView.as_view(), name = 'job-list'),
    
    # change password urls
    url(r'^password-change/$', password_change, name='password_change'),
    url(r'^password-change/done/$', password_change_done, name='password_change_done'),

    # restore password urls
    url(r'^password-reset/$', password_reset, name='password_reset'),
    url(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),
]