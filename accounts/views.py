from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from accounts.models import UserService, Service, JobLanguage, UserAccount, WorkIndustry, Industry, WorkExperience, Education, Institute, Skill, HardSkill, UserLanguage, Link, Job, Language, Price
from django.core.urlresolvers import reverse
import datetime
from django.utils import timezone

from django.conf import settings
from_email = settings.EMAIL_HOST_USER
regisration_admins = settings.REGISTRATION_ADMINS
contact_admins = settings.CONTACT_ADMINS
from django_countries import countries
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import login
#import gender_guesser.detector as gender
from django.contrib.auth.decorators import login_required
from common.models import Location, Article, NewsLetterEmail, ServiceAlert
from common.tools import str_only

from django.core.files.storage import FileSystemStorage
from django.core.files import File
import random
from django.db.models import Q
from django.middleware.csrf import get_token
from django.views.generic.list import ListView
from django.utils import timezone
from accounts.models import Job

class JobListView (ListView):
	model = Job

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['now'] = timezone.now()
		return context


@login_required
def redirect_account_connection(request):
	return HttpResponseRedirect('/register/social-links')

def employer_employee_redirect(profile, category):
	if profile.category != category:
		if profile.category == 'Job Seeker':
			return reverse('profile_page')
		elif profile.category == 'Employer':
			return reverse('employer_page')
		elif profile.category == 'Service Provider':
			return reverse('service_provider')
		elif profile.category == 'Service Seeker':
			return reverse('service_seeker')

	return None

def employer_profile_check(profile):
	if profile.application_details == False:
		return reverse('application_questions')

@login_required
def delete_service(request, service_id, template_name="delete-service.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()

	exists = UserService.objects.filter(id=service_id, active=True, profile=profile)

	if exists:
		context['service'] = exists[0]

	return render_to_response(template_name, context)

def contact_provider(request, service_id, template_name="contact-provider.html"):
	context = RequestContext(request)

	email = request.GET.get('email', None)
	exists = UserService.objects.filter(id=service_id, active=True)

	if request.user.is_authenticated():
		context['profile'] = profile = request.user.profile.first()

	if exists and email:
		context['status'] = True

		data = {}
		data['service'] = service = exists[0]

		html_body = render_to_string('emails/service.html', data)
		body = render_to_string('emails/service.txt', data)
		msg = EmailMultiAlternatives("KaziLynk Service: {0} {1}".format(service.service.name, service.company_name), body, from_email, [email])
		msg.attach_alternative(html_body, "text/html")
		msg.send()

		body = render_to_string('emails/new-service-request.txt', data)
		msg = EmailMessage('Kazilynk: Someone is interested in your service', body, from_email, [service.email])
		msg.send()

	else:
		context['status'] = False

	return render_to_response(template_name, context)

@login_required
def view_profile(request, user_id, template_name="view-profile.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()

	exists = UserAccount.objects.filter(id=user_id)

	if exists:
		user = exists[0]
		context['user_profile'] = user

	return render_to_response(template_name, context)

@login_required
def delete_job(request, job_id, template_name="delete-job.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()

	exists = Job.objects.filter(id=job_id, active=True, profile=profile)

	if exists:
		context['job'] = exists[0]

	return render_to_response(template_name, context)

@login_required
def edit_service(request, service_id, template_name="edit-service.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()

	context['service_id'] = request.COOKIES.get('service_id', None)

	context['services'] = Service.objects.filter(active=True).order_by('name')
	context['locations'] = Location.objects.filter(country=False).order_by('country','name', 'country_name')

	exists = UserService.objects.filter(id=service_id, active=True, profile=profile)

	if exists:
		context['service'] = exists[0]

	response = render_to_response(template_name, context)
	response.set_cookie('service_id', service_id)

	return response

@login_required
def edit_job(request, job_id, template_name="edit-job.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()

	exists = Job.objects.filter(id=job_id, active=True, profile=profile)

	context['countries'] = location_list(is_country=False)
	context['skills'] = Skill.objects.filter(active=True).order_by('name')
	context['hardskills'] = HardSkill.objects.filter(active=True).order_by('name')
	context['institutions'] = Institute.objects.filter(active=True).order_by('name')

	if exists:
		context['job'] = exists[0]

	return render_to_response(template_name, context)

def view_service(request, service_id, template_name="view-service.html"):
	context = RequestContext(request)

	exists = UserService.objects.filter(id=service_id, active=True)

	if exists:
		context['service'] = service = exists[0]

		if request.user.is_authenticated():
			context['profile'] = profile = request.user.profile.first()
			context['author'] = profile == service.profile

	return render_to_response(template_name, context)	

def view_job(request, job_id, template_name="view-job.html"):
	context = RequestContext(request)

	if request.user.is_authenticated():
		context['profile'] = profile = request.user.profile.first()

	try:
		now = datetime.date.today()
		job = Job.objects.get(id=job_id, active=True, end_date__gte=now)

		if job:
			user = request.user
			if user not in job.viewers.all():
				job.viewers.add(user)
				job.save()
			context['job'] = job
		else:
			pass

	except:
		pass

	return render_to_response(template_name, context)	

def employer_page(request, template_name="accounts/employer_page.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()
	context['jobs'] = [x for x in profile.jobs.filter(active=True) if x.expired() == False]

	redirect_url = employer_profile_check(profile)

	if redirect_url:
		return HttpResponseRedirect(redirect_url)

	redirect = employer_employee_redirect(profile, category='Employer')
	if redirect:
		return HttpResponseRedirect(redirect)

	if request.method == 'POST' and request.FILES['prof-pic']:
		prof_pic = request.FILES['prof-pic']
		fs = FileSystemStorage()
		filename = fs.save('logo_upload/' + prof_pic.name, prof_pic)
			
		profile.company_logo = File( open('django_project/media/' + filename, 'r') )
		profile.save()

	return render_to_response(template_name, context)

def add_service(request, template_name="accounts/add-service.html"):
	context = RequestContext(request)
	context['services'] = Service.objects.filter(active=True).order_by('name')
	context['locations'] = Location.objects.filter(country=False).order_by('country','name', 'country_name')

	return render_to_response(template_name, context)

def service_provider_page(request, template_name="accounts/service-provider-page.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()

	redirect = employer_employee_redirect(profile, category='Service Provider')
	if redirect:
		return HttpResponseRedirect(redirect)

	if request.method == 'POST' and request.FILES['prof-pic']:
		prof_pic = request.FILES['prof-pic']
		fs = FileSystemStorage()
		filename = fs.save('profile_pic/' + prof_pic.name, prof_pic)
			
		profile.image = File( open('django_project/media/' + filename, 'r') )
		profile.save()

	return render_to_response(template_name, context)

def service_seeker_page(request, template_name="accounts/service-seeker-page.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()

	redirect = employer_employee_redirect(profile, category='Service Seeker')
	if redirect:
		return HttpResponseRedirect(redirect)

	return render_to_response(template_name, context)

def my_jobs_view(request, template_name="accounts/profile_jobs.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()

	redirect_url = employer_profile_check(profile)

	if redirect_url:
		return HttpResponseRedirect(redirect_url)

	context['countries'] = location_list(is_country=False)
	context['skills'] = Skill.objects.filter(active=True).order_by('name')
	context['hardskills'] = HardSkill.objects.filter(active=True).order_by('name')
	context['institutions'] = Institute.objects.filter(active=True).order_by('name')

	return render_to_response(template_name, context)


def application_questions(request, template_name="accounts/application_questions.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()
	profile.save()

	if profile.profile_complete == False:
		redirect_url = reverse('user_details')
		return HttpResponseRedirect(redirect_url)

	context['countries'] = location_list(is_country=False)
	context['skills'] = Skill.objects.filter(active=True).order_by('name')
	context['hardskills'] = HardSkill.objects.filter(active=True).order_by('name')
	context['institutions'] = Institute.objects.filter(active=True).order_by('name')

	return render_to_response(template_name, context)

def social_provider(request, update=False, profile=None):
	google = SocialAccount.objects.filter(provider='google', user_id=request.user.id).first()
	facebook = SocialAccount.objects.filter(provider='facebook', user_id=request.user.id).first()
	twitter = SocialAccount.objects.filter(provider='twitter', user_id=request.user.id).first()
	stackoverflow = SocialAccount.objects.filter(provider='stackexchange', user_id=request.user.id).first()
	linkedin = SocialAccount.objects.filter(provider='linkedin_oauth2', user_id=request.user.id).first()

	response = {'exists': False}

	if google:
		response['provider'] = 'google'
		response['exists'] = True

		data = google.extra_data

		response['first_name'] = first_name = data['name']
		response['last_name'] = data['family_name']
		response['profile_pic_img'] = data['picture']
		response['email'] = data['email']

		gender_pred = gender.Detector()
		response['gender'] = gender_pred.get_gender(first_name)

	elif facebook:
		response['provider'] = 'facebook'
		response['exists'] = True

		data = facebook.extra_data

		response['first_name'] = data['first_name']
		response['last_name'] = data['last_name']
		response['gender'] = data['gender']
		response['profile_pic_img'] = None
		#email = response['email']

	elif twitter:
		response['provider'] = 'twitter'
		response['exists'] = True

		data = twitter.extra_data

		response['profile_pic_img'] = data['profile_image_url_https']
		response['country'] = data['location']

	elif stackoverflow:
		response['provider'] = 'stackoverflow'
		response['exists'] = True

	elif linkedin:
		response['provider'] = 'linkedin'
		response['exists'] = True

		data = linkedin.extra_data

		response['first_name'] = first_name = data['firstName']
		response['last_name'] = data['lastName']
		response['profile_pic_link'] = data['pictureUrl']
		#response['email'] = data['email']

		gender_pred = gender.Detector()
		response['gender'] = gender_pred.get_gender(first_name)

	if update and profile:
		if response['provider'] == 'linkedin':
			profile.first_name = response['first_name']
			profile.last_name = response['last_name']

		elif response['provider'] == 'stackoverflow':
			pass

		elif response['provider'] == 'twitter':
			pass

		elif response['provider'] == 'facebook':
			profile.first_name = response['first_name']
			profile.last_name = response['last_name']
			profile.gender = response['gender'].capitalize()

		elif response['provider'] == 'google':
			profile.first_name = response['first_name']
			profile.last_name = response['last_name']
			profile.gender = response['gender'].capitalize()

		profile.save()
		response['profile_update'] = True

	elif update:
		response['profile_update'] = False

	return response

def location_list(is_country=None):
	locations = Location.objects.all().order_by('country','name', 'country_name')

	if is_country==True or is_country == False:
		locations = locations.filter(country=is_country)
	response_list = []

	for item in locations:
		if item.country:
			response_list.append([item.country_code, item.country_name])
		else:
			response_list.append([item.name, item.name])

	return response_list

def confirm_verification(request, user_id, code, template_name='accounts/confirm_verification.html'):
	context = RequestContext(request)

	try:
		user = User.objects.get(id=user_id)
		profile = user.profile.first()
		today = timezone.now()
		validation_key = profile.email_verification_code
		expiry = profile.email_validation_expire

		if profile.category == 'Employer' and profile.profile_complete == False:
			profile.profile_complete = True
			profile.save()

		context['profile'] = profile
		context['services'] = Service.objects.filter(active=True).order_by('name')
		context['locations'] = Location.objects.filter(country=False).order_by('country','name', 'country_name')

		if profile.category == 'Employer':
			context['employer'] = True
		elif profile.category == 'Job Seeker':
			context['job_seeker'] = True
		elif profile.category == 'Service Provider':
			context['service_provider'] = True
		elif profile.category == 'Service Seeker':
			context['service_seeker'] = True

		if code == validation_key and expiry > today:
			user.is_active = True
			user.save()
			context['verified'] = True
			context['countries'] = list(countries)

			now = timezone.now()
			context['user_id'] = user_id
			context['verification_code'] = code
			context['industries'] = WorkIndustry.objects.filter(active=True, start_time__lte=now).order_by('name')

			request.user = user

			return HttpResponseRedirect('/accounts/login/')
				

		elif expiry < today:
			context['error'] = "Link has expired. <a href=''>Click Here</a> to receive a new link."
			#create link for automatically sending new confirmation email
		elif code != validation_key:
			context['error'] = "Key Validation Failed. Please try using the forgot password to create a new link."

	except:
		context['error'] = "Link Invalid, Please try using the forgot password to create a new link."

	response = render_to_response(template_name, context)
	token = get_token(request)
	response.set_cookie('csrftoken', token)

	return response

def register(request, template_name="accounts/register.html"):
	context = RequestContext(request)
	response = render_to_response(template_name, context)
	token = get_token(request)
	response.set_cookie('csrftoken', token)

	return response

def education_form(request, template_name="snippets/education_form.html"):
	context = RequestContext(request)
	context['institutions'] = Institute.objects.filter(active=True).order_by('name')
 
	return render_to_response(template_name, context)

def socialauth(request, template_name="accounts/social_auth.html"):
	context = RequestContext(request)
	return render_to_response(template_name, context)

def contact_send(request):
	response = {'status': None}
	if request.method == 'POST':
		data = json.loads(request.body)
		email, email_type, message = data['email'], data['email-type'], data['message']

		context = {
			'email': email,
			'email_type': email_type,
			'message': message
		}

		body = render_to_string('emails/contact.txt', context)

		msg = EmailMessage('Kazilynk: message from contact us form', body, from_email, contact_admins)
		msg.send()

		response['status'] = 'ok'
	else:
		response['error'] = 'No Post Data Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)		

def post_job(request):
	response = {'status': None}
	if request.method == 'POST':
		data = json.loads(request.body)
		job_title, responsibility, industry, job_level, job_type, end_date, start_date = data['job-title'], data['responsibility'], data['industry'], data['job-level'], data['job-type'], data['end-date'], data['start-date']

		end_date = end_date.split('/')

		if len(end_date) != 3:
			end_date = None

		start_date = start_date.split('/')

		if len(start_date) != 3:
			start_date = None

		if start_date:
			start_date = [int(x) for x in start_date]
			start_dt = datetime.datetime(start_date[-1], start_date[-3], start_date[-2])
		else:
			start_date = datetime.date.today()

		if end_date:
			end_date = [int(x) for x in end_date]
			date = datetime.datetime(end_date[-1], end_date[-3], end_date[-2])
		else:
			date = datetime.datetime.today() + datetime.timedelta(days=14)

		profile = request.user.profile.first()

		job = Job(start_date=start_dt, end_date=date, profile=profile, job_title=job_title, responsibility=responsibility, industry=industry, job_level=job_level, job_type=job_type)
		job.save()

		response['status'] = 'ok'
	else:
		response['error'] = 'No Post Data Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)


def complete(request, template_name="accounts/complete.html"):
	context = RequestContext(request)
	return render_to_response(template_name, context)

@login_required
def user_details(request, template_name="accounts/confirm_verification.html"):
	context = RequestContext(request)

	context['employer'] = False
	context['job_seeker'] = False

	if request.user.profile.first():
		if request.user.profile.first().profile_complete == True:
			return HttpResponseRedirect('/accounts/profile')
		else:
			context['profile'] = profile = request.user.profile.first()

			if profile.category == 'Employer':
				context['employer'] = True
			elif profile.category == 'Job Seeker':
				context['job_seeker'] = True
			elif profile.category == 'Service Provider':
				context['service_provider'] = True
			elif profile.category == 'Service Seeker':
				context['service_seeker'] = True
	
	
	now = timezone.now()
	context['verified'] = True
	context['countries'] = list(countries)
	context['industries'] = WorkIndustry.objects.filter(active=True, start_time__lte=now).order_by('name')
	context['services'] = Service.objects.filter(active=True).order_by('name')
	context['locations'] = Location.objects.filter(country=False).order_by('country','name', 'country_name')
	return render_to_response(template_name, context)

@login_required
def job_criteria(request, template_name="accounts/job_criteria.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()
	context['countries'] = location_list(is_country=False)
	context['prev'] = reverse('profile_details')
	context['next'] = reverse('work_experience')

	context['industry_list'] = [str_only(x.name) for x in profile.industry.all()]

	return render_to_response(template_name, context)

@login_required
def work_experience(request, template_name="accounts/work_experience.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()
	context['work_exps'] = profile.experience.filter(active=True)
	context['prev'] = reverse('job_criteria')
	context['next'] = reverse('education')


	return render_to_response(template_name, context)

@login_required
def education(request, template_name='accounts/education.html'):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()
	context['education_exp'] = profile.education.filter(active=True)
	context['institutions'] = Institute.objects.filter(active=True).order_by('name')
	context['prev'] = reverse('work_experience')
	context['next'] = reverse('skills')

	return render_to_response(template_name, context)

@login_required
def skills(request, template_name="accounts/skills.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()
	context['skills'] = Skill.objects.filter(active=True).order_by('name')
	context['hard_skills'] = HardSkill.objects.filter(active=True).order_by('name')

	context['prev'] = reverse('education')
	context['next'] = reverse('language')

	context['skills_list'] = [str_only(x.name) for x in profile.skills.filter(active=True)]
	context['hard_skills_list'] = [str_only(x.name) for x in profile.hard_skills.filter(active=True)]

	return render_to_response(template_name, context)

@login_required
def language(request, template_name="accounts/language.html"):
	context = RequestContext(request)

	context['profile'] = profile =request.user.profile.first()
	context['language_exp'] = profile.languages.filter(active=True)
	context['prev'] = reverse('skills')
	context['next'] = reverse('documents')

	return render_to_response(template_name, context)

@login_required
def documents(request, template_name="accounts/documents.html"):
	context = RequestContext(request)

	context['profile'] = profile =request.user.profile.first()
	context['links'] = profile.links.filter(active=True)

	context['prev'] = reverse('language')

	if request.method == 'POST' and request.FILES['cv']:
		cv = request.FILES['cv']
		fs = FileSystemStorage()
		filename = fs.save('documents/' + cv.name, cv)
			
		profile.document = filename
		profile.save()

	return render_to_response(template_name, context)

@login_required
def social_links(request, template_name="accounts/social_links.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()

	return render_to_response(template_name, context)

def search(request, template_name="search.html"):
	context = RequestContext(request)

	if request.user.is_authenticated():
		context['profile'] = profile = request.user.profile.first()

	return render_to_response(template_name, context)

def home(request, template_name="homepage.html"):
	context = RequestContext(request)

	if request.user.is_authenticated():
		context['profile'] = profile = request.user.profile.first()

	context['articles'] = Article.objects.filter(active=True, on_homepage=True).order_by('id')[:4]
	context['home_page_cookie_js'] = '<script type="text/javascript" src="/static/js/jquery.cookie.min.js"></script>'

	return render_to_response(template_name, context)

def check_post_job(request, template_name="accounts/check-post-job.html"):
 	context = RequestContext(request)

 	if not request.user.is_authenticated():
 		redirect_url = reverse('register')
 		return HttpResponseRedirect(redirect_url)

 	context['profile'] = profile = request.user.profile.first()

 	if profile.category == 'Employer':
		 isinstance (profile, str)
		 url = reverse('create_job')
 		 return HttpResponseRedirect(url)

 	return render_to_response(template_name, context)


def check_post_cv(request, template_name="accounts/check-user-needed.html"):
	context = RequestContext(request)

	if not request.user.is_authenticated():
		redirect_url = reverse('register') + '?click=job-seeker'
		return HttpResponseRedirect(redirect_url)

	context['desired_user'] = desired_user = 'Job Seeker'
	context['profile'] = profile = request.user.profile.first()
	context['intent'] = 'CV'

	if profile.category == desired_user:
		url = reverse('documents')
		return HttpResponseRedirect(url)

	return render_to_response(template_name, context)


def check_post_service(request, template_name="accounts/check-user-needed.html"):
	context = RequestContext(request)

	if not request.user.is_authenticated():
		redirect_url = reverse('register') + '?click=service-providers'
		return HttpResponseRedirect(redirect_url)

	context['desired_user'] = desired_user = 'Service Provider'
	context['profile'] = profile = request.user.profile.first()
	context['intent'] = 'Service'

	if profile.category == desired_user:
		url = reverse('add_service')
		return HttpResponseRedirect(url)

	return render_to_response(template_name, context)

@login_required
def change_user_type(request, template_name="change-user-type.html"):
	context = RequestContext(request)

	context['profile'] = profile = request.user.profile.first()

	return render_to_response(template_name, context)

@login_required
def profile_userdetails(request, template_name="accounts/user_details.html"):
	context = RequestContext(request)

	context['profile'] = request.user.profile.first()
	context['countries'] = location_list(is_country=True)
	context['next'] = reverse('job_criteria')

	return render_to_response(template_name, context)

def profile(request, template_name="accounts/profile.html"):
	context = RequestContext(request)

	if request.user.is_authenticated() == False:
		return HttpResponseRedirect('/accounts/login')
	elif request.user.profile.first():
		profile = request.user.profile.first()

		if profile.category == 'Employer' and profile.profile_complete == False:
			profile.profile_complete = True
			profile.save()
			
		elif profile.profile_complete == False:
			return HttpResponseRedirect('/register/user-details')

	elif not request.user.profile.first():
		return HttpResponseRedirect('/register/user-details')

	context['special_css'] = 'no-padding-bottom'

	context['profile'] = profile = request.user.profile.first()

	context['country_name'] = ''

	if profile.country:
		exists = Location.objects.filter(country_code=profile.country)

		if exists:
			country = exists[0]

			context['country_name'] = country.country_name

	social_auth = social_provider(request)

	if not profile.first_name and social_auth['exists']:
		social_provider(request, update=True, profile=profile)

	if request.method == 'POST' and request.FILES['prof-pic']:
		prof_pic = request.FILES['prof-pic']
		fs = FileSystemStorage()
		filename = fs.save('profile_pic/' + prof_pic.name, prof_pic)
			
		profile.image = File( open('django_project/media/' + filename, 'r') )
		profile.save()

	redirect = employer_employee_redirect(profile, category='Job Seeker')
	if redirect:
		return HttpResponseRedirect(redirect)

	return render_to_response(template_name, context)

def deactivate_industry(request, work_id, code, template_name="accounts/deactivate_industry.html"):
	context = RequestContext(request)

	industry_exists = WorkIndustry.objects.filter(id=work_id)
	if industry_exists:
		industry = industry_exists.first()
		if code == industry.verification_code:
			industry.active = False
			industry.save()

			context['complete'] = True
		else:
			context['error_message'] = "Link Code Validation Failed"
	else:
		context['error_message'] = "No Record of the Industry can be found"

	return render_to_response(template_name, context)

def lynkspiration(request, template_name="lynkspiration.html"):
	context = RequestContext(request)
	articles = Article.objects.filter(active=True, top_article=True).order_by('id')

	if articles:
		context['article'] = articles[0]

		context['popular'] = popular =Article.objects.filter(active=True, popular=True).order_by('id')[:5]
		context['next_article'] = random.choice(popular)

	response = render_to_response(template_name, context)
	token = get_token(request)
	response.set_cookie('csrftoken', token)
	return response

def view_article(request, slug, template_name="view-article.html"):
	context = RequestContext(request)

	slug_text = slug.replace('-',' ')
	exists = Article.objects.filter(active=True, slug=slug_text)

	if exists:
		context['article'] = article = exists[0]
		context['popular'] = popular =Article.objects.filter(active=True, popular=True).exclude(id=article.id).order_by('id')[:5]
		context['next_article'] = random.choice(popular)

	response = render_to_response(template_name, context)
	token = get_token(request)
	response.set_cookie('csrftoken', token)
	return response

def activate_industry(request, work_id, code, template_name="accounts/activate_industry.html"):
	context = RequestContext(request)

	industry_exists = WorkIndustry.objects.filter(id=work_id)
	if industry_exists:
		industry = industry_exists.first()
		if code == industry.verification_code:
			push_time = timezone.now() - datetime.timedelta(seconds=7200)
			
			industry.start_time = push_time
			industry.active = True
			industry.save()
			context['complete'] = True
		else:
			context['error_message'] = "Link Code Validation Failed"

	else:
		context['error_message'] = "No Record of the Industry can be found"

	return render_to_response(template_name, context)

def service_provider(request):
	response = {'status': None}
	if request.method == 'POST':
		data = json.loads(request.body)
		negotiable, company_name, email, phone_no, company_website, location, service, testimonial, charge, business_details = data['rates-negotiable'], data['company-name'], data['email'], data['phone-no'], data['company-website'], data['location'], data['service'], data['testimonial'], data['charge'], data['business-details']
		links, prices = data['links'], data['prices']

		email = email.lower()
		exists = Service.objects.filter(name=service)

		if exists:
			service = exists[0]
		else:
			service = Service(name=service)
			service.save()

		profile = request.user.profile.first()

		user_service = UserService(service=service, negotiable=negotiable, company_name=company_name, email=email, phone=phone_no, company_website=company_website, location=location, testimonial=testimonial, price=charge, business_details=business_details)
		user_service.save()

		for key in links.keys():
			link = links[key]
			link = Link(link=link['link'], link_info=link['link-info'], profile=profile)
			link.save()

			user_service.links.add(link)

		for key in prices.keys():
			price = prices[key]
			price = Price(name=price['price'])
			price.save()

			user_service.prices.add(price)

		user_service.save()

		profile.profile_complete = True
		profile.services.add(user_service)
		profile.save()

		location_cap = location.capitalize()
		exists = Location.objects.filter(Q(name=location) | Q(name=location_cap))

		if not exists:
			new = Location(name=location_cap)
			new.save()

		response['redirect-url'] = reverse('service_provider')
		response['service-id'] = user_service.id
		response['upload-url'] = reverse('upload-new')
		response['status'] = 'ok'
	else:
		response['error'] = 'No Post Data Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)


def update_category(request):
	response = {'status': None}
	if request.method == 'POST':
		post_data = json.loads(request.body)

		category = post_data['category']

		if request.user.is_active == True:
			profile = request.user.profile.first()

			if not profile:
				profile = UserAccount(user=request.user, profile_complete=True)
				profile.save()
				
			profile.category = category
			profile.save()
			response['status'] = "OK"
		else:
			response['status'] = "OK"

	else:
		response['error'] = 'No Post Data Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def edit_job_ajax(request):
	response = {'status': None}
	if request.method == 'POST':
		data = json.loads(request.body)

		company_name, company_size, job_title, responsibility, job_type, min_salary, max_salary, job_level, start_date, end_date, work_location, education_level, institutions, personality, training, work_experience, skills, hard_skills, languages, contacts, job_id = data['company-name'], data['company-size'], data['job-title'], data['responsibility'], data['job-type'], data['min-salary'], data['max-salary'], data['job-level'], data['start-date'], data['end-date'], data['work-location'], data['education-level'], data['institutions'], data['personality'], data['training'], data['work-experience'], data['skills'], data['hard-skills'], data['languages'], data['contacts'], data['job-id']

		if request.user.is_authenticated():
			profile = request.user.profile.first()

			allowed = Job.objects.filter(active=True, profile=profile, id=job_id)

			if allowed:
				job = allowed[0]

				if job_title:
					job.job_title = job_title

				if company_name:
					job.company_name = company_name

				if company_size:
					job.company_size = company_size

				if responsibility:
					job.responsibility = responsibility

				if job_type:
					job.job_type = job_type

				if min_salary:
					job.min_salary = min_salary

				if max_salary:
					job.max_salary = max_salary

				if job_level:
					job.job_level = job_level

				if start_date:
					date_split = start_date.split('/')

					if len(date_split) == 3:
						month,day,year = [int(x) for x in date_split]
						start_dt = datetime.date(day=day, month=month, year=year)
					else:
						start_dt = None

					if start_dt:
						job.start_date = start_dt

				if end_date:
					date_split = end_date.split('/')

					if len(date_split) == 3:
						month,day,year = [int(x) for x in date_split]
						end_dt = datetime.date(day=day, month=month, year=year)
					else:
						end_dt = None

					if end_dt:
						job.end_date = end_dt

				if work_location:
					job.work_location = work_location

				if education_level:
					job.education_level = education_level

				if institutions:
					job.institutions.clear()
					is_list = type(institutions) == list

					if is_list:
						for institute in institutions:
							exists = Institute.objects.filter(name=institute)

							if exists:
								inst_db = exists[0]
							else:
								inst_db = Institute(name=institute)
								inst_db.save()

							if inst_db not in job.institutions.all():
								job.institutions.add(inst_db)

					else:
						exists = Institute.objects.filter(name=institutions)

						if exists:
							inst_db = exists[0]
						else:
							inst_db = Institute(name=institute)
							inst_db.save()

						if inst_db not in job.institutions.all():
							job.institutions.add(inst_db)

				if personality:
					job.personality = personality

				if training:
					job.training = training

				if work_experience:
					job.work_experience = work_experience

				if skills:
					profile.skills.clear()

					for skill in skills:
						exists = Skill.objects.filter(name__contains=skill)

						if exists:
							skill_id = exists[0].id
							profile.skills.add(skill_id)

						else:
							new_skill = Skill(name=skill)
							new_skill.save()

							profile.skills.add(new_skill.id)

				if hard_skills:
					profile.hard_skills.clear()

					for skill in hard_skills:
						exists = HardSkill.objects.filter(name__contains=skill)

						if exists:
							skill_id = exists[0].id
							profile.hard_skills.add(skill_id)

						else:
							new_skill = HardSkill(name=skill)
							new_skill.save()

							profile.hard_skills.add(new_skill.id)

				if languages:
					job.languages.clear()

					keys = languages.keys()

					for key in keys:
						exp = languages[key]
						language, reading_level, writing_level, verbal_level = exp['language'], exp['reading-level'], exp['writing-level'], exp['verbal-level']

						la_db = JobLanguage(name=language)

						if reading_level:
							la_db.reading_level = reading_level

						if writing_level:
							la_db.writing_level = writing_level

						if verbal_level:
							la_db.verbal_level = verbal_level

						data_exists = reading_level or writing_level or verbal_level and language

						if data_exists:
							la_db.save()
							job.languages.add(la_db)

				if contacts:
					job.contacts = contacts

				job.save()

				response['status'] = 'OK'
			else:
				response['error'] = 'Not allowed to edit job post'

		else:
			response['error'] = 'Not Logged In'

	else:
		response['error'] = 'No Post Data Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def update_user_type(request):
	response = {'status': None}
	if request.method == 'POST':
		post_data = json.loads(request.body)

		user_type = post_data['user-type']

		profile = request.user.profile.first()
		profile.category = user_type
		profile.save()
		response['status'] = 'ok'		

	else:
		response['error'] = 'No Post Data Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def delete_service_ajax(request):
	response = {'status': None}
	if request.method == 'POST':
		data = json.loads(request.body)

		service_id = data['service-id']
		profile = request.user.profile.first()

		allowed = UserService.objects.filter(active=True, profile=profile, id=service_id)

		if allowed:
			service = allowed[0]

			service.active = False
			service.save()

			response['status'] = 'ok'

		else:
			response['error'] = 'Access Denied'

	else:
		response['error'] = 'No Post Data Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)


def delete_job_ajax(request):
	response = {'status': None}
	if request.method == 'POST':
		data = json.loads(request.body)

		job_id = data['job-id']
		profile = request.user.profile.first()

		allowed = Job.objects.filter(active=True, profile=profile, id=job_id)

		if allowed:
			job = allowed[0]

			job.active = False
			job.save()

			response['status'] = 'ok'

		else:
			response['error'] = 'Access Denied'

	else:
		response['error'] = 'No Post Data Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def signup_newsletter(request):
	response = {'status': None}
	if request.method == 'POST':
		post_data = json.loads(request.body)

		email = post_data['email']

		exists = NewsLetterEmail.objects.filter(email=email)

		response['status'] = 'ok'
		if exists:
			response['message'] = "Email was already added to newsletter"

		else:
			new = NewsLetterEmail(email=email)
			new.save()

			user_json = {'email': email}
			body = render_to_string('emails/new_user.txt', user_json)
			msg = EmailMessage('New User for NewsLetter', body, from_email, regisration_admins)
			msg.send()

			response['message'] = "Email added to newsletter"

	else:
		response['error'] = 'No Post Data Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def profile_update(profile, post_data):
	try:
		
		first_name, last_name, heard_from, other_source, phone, country_code, phone_code = post_data['first_name'], post_data['last_name'], post_data['heard-from'], post_data['other-source'], post_data['phone'], post_data['country'], post_data['phone-code']
		
		if first_name:
			profile.first_name = first_name
		
		if last_name:
			profile.last_name = last_name

		if other_source:
			heard_from = other_source
		
		if heard_from:
			profile.heard_from = heard_from

		if phone:
			profile.phone = phone

		if country_code:
			profile.country = country_code

		if phone_code:
			profile.phone_code = phone_code
		
		profile.save()
		return {'status': True}
	except Exception, e:
		return {'status': False, 'error_type': str(repr(e))}


def job_criteria_save(profile, post_data):
	try:

		personal_statement, company_size, work_location, job_level, available, min_salary, max_salary, currency = post_data['personal-statement'], post_data['company-size'], post_data['work-location'], post_data['job-level'], post_data['available'], post_data['min-salary'], post_data['max-salary'], post_data['currency']
		
		if personal_statement:
			profile.personal_statement = personal_statement

		if company_size:
			profile.company_size = company_size

		if work_location:
			profile.work_location = work_location

		if job_level:
			profile.job_level = job_level

		if available:
			profile.availability = available

		if min_salary:
			profile.min_salary = min_salary

		if max_salary:
			profile.max_salary = max_salary

		if currency:
			profile.salary_currency = currency

		profile.save()
		return {'status': True}

	except Exception, e:
		return {'status': False, 'error_type': repr(e)}

def work_experience_save(profile, post_data):
	try:
		experience, demote = post_data['work-experience'], post_data['remove']

		keys = experience.keys()

		for key in keys:
			item = experience[key]
			exists, company_name, job_title, responsibility, achievements, exp_id = item['exp-id'], item['company-name'], item['job-title'], item['responsibility'], item['achievements'], item['exp-id']

			data_exists = company_name or job_title or responsibility or achievements or start_date or end_date

			if exists and 'new' not in exists:
				exp = WorkExperience.objects.get(id= exp_id, profile= profile)
			else:
				exp = WorkExperience(profile=profile)

			if company_name:
				exp.company_name = company_name

			if job_title:
				exp.job_title = job_title

			if responsibility:
				exp.responsibility = responsibility

			if achievements:
				exp.achievements = achievements

			if data_exists:
				exp.save()

		for key in demote:
			exp = WorkExperience.objects.get(id=key, profile= profile)
			exp.active = False
			exp.save()

		return {'status': True}
	except Exception, e:
		return {'status': False, 'error_type': repr(e)}

def education_save(profile, post_data):
	try:
		experience, demote = post_data['education'], post_data['remove']

		keys = experience.keys()

		for key in keys:
			item = experience[key]
			exp_id, education_level, other_level, name = item['exp-id'], item['education-level'], item['other-level'], item['name']

			data_exists = education_level or other_level or name

			if exp_id and 'new' not in exp_id:
				exp = Education.objects.get(id=exp_id, profile=profile)
			else:
				exp = Education(profile=profile)

			if education_level == 'other':
				education_level = other_level

			if education_level:
				exp.level = education_level

			if name:
				name = name.title()
				exists = Institute.objects.filter(name=name)

				if exists:
					institute = exists[0]
				else:
					institute = Institute(name=name)
					institute.save()

				exp.institute = institute

			if data_exists:
				exp.save()

		for key in demote:
			exp = Education.objects.get(id=key, profile=profile)
			exp.active = False
			exp.save()

		profile.save()
		return {'status': True}
	except Exception, e:
		return {'status': False, 'error_type': repr(e)}

def skill_save(profile, post_data):
	try:
		skills, hard_skills = post_data['skills'], post_data['hard-skills']

		if skills:
			profile.skills.clear()

			for skill in skills:
				exists = Skill.objects.filter(name__contains=skill)

				if exists:
					skill_id = exists[0].id
					profile.skills.add(skill_id)

				else:
					new_skill = Skill(name=skill)
					new_skill.save()

					profile.skills.add(new_skill.id)


		if hard_skills:
			profile.hard_skills.clear()

			for skill in hard_skills:
				exists = HardSkill.objects.filter(name__contains=skill)

				if exists:
					skill_id = exists[0].id
					profile.hard_skills.add(skill_id)

				else:
					new_skill = HardSkill(name=skill)
					new_skill.save()

					profile.hard_skills.add(new_skill.id)

		profile.save()
		return {'status': True}
	except Exception, e:
		return {'status': False, 'error_type': repr(e)}


def language_save(profile, post_data):
	try:
		languages, demote = post_data['languages'], post_data['remove']

		keys = languages.keys()

		for key in keys:
			item = languages[key]

			language, reading_level, verbal_level, writing_level, exp_id, new_language = item['language'], item['reading-level'], item['verbal-level'], item['writing-level'], item['exp-id'], item['new-language']

			data_exists = language or reading_level or verbal_level or writing_level

			if exp_id and 'new' not in exp_id:
				exp = UserLanguage.objects.get(id=exp_id, profile=profile)
			else:
				exp = UserLanguage(profile=profile)

			if language == 'other':
				language = new_language

			if language:
				exp.language = language

			if reading_level:
				exp.reading_level = reading_level

			if verbal_level:
				exp.verbal_level = verbal_level

			if writing_level:
				exp.writing_level = writing_level

			if data_exists:
				exp.save()		

		for key in demote:
			exp = UserLanguage.objects.get(id=key, profile=profile)
			exp.active = False
			exp.save()

		profile.save()
		return {'status': True}
	except Exception, e:
		return {'status': False, 'error_type': repr(e)}

def links_save(profile, post_data):
	try:
		links, demote = post_data['links'], post_data['remove-links']

		link_keys = links.keys()

		for key in link_keys:
			item = links[key]

			link, link_info, exp_id = item['link'], item['link-info'], item['exp-id']

			data_exists = link or link_info

			if exp_id and 'new' not in exp_id:
				exp = Link.objects.get(id=exp_id, profile=profile)
			else:
				exp = Link(profile=profile)

			if link:
				exp.link = link

			if link_info:
				exp.link_info = link_info

			if data_exists:
				exp.save()			


		for key in demote:
			exp = Link.objects.get(id=key, profile=profile)
			exp.active = False
			exp.save()

		profile.save()
		return {'status': True}			
	except Exception, e:
		return {'status': False, 'error_type': repr(e)}

def employer_save(profile, post_data):
	try:
		company_size, company_name = post_data['company-size'], post_data['company-name']

		profile.company_name = company_name
		profile.company_size = company_size

		profile.profile_complete = True
		profile.save()
		return {'status': True}			
	except Exception, e:
		return {'status': False, 'error_type': repr(e)}

def job_save(profile, post_data):
	try:
		work_location, education_level, institutions, training, work_experience, skills, languages, contacts = post_data['work-location'], post_data['education-level'], post_data['institution'], post_data['training'], post_data['work-experience'], post_data['skills'], post_data['languages'], post_data['contacts']
		company_name, company_size, currency, job_title, responsibility, job_type, min_salary, max_salary, job_level, start_date, end_date, personality, hard_skills = post_data['company-name'], post_data['company-size'], post_data['currency'], post_data['job-title'], post_data['responsibility'], post_data['job-type'], post_data['min-salary'], post_data['max-salary'], post_data['job-level'], post_data['start-date'], post_data['end-date'], post_data['personality'], post_data['hard-skills']

		if start_date:
			date_split = start_date.split('/')

			if len(date_split) == 3:
				month,day,year = [int(x) for x in date_split]
				start_dt = datetime.date(day=day, month=month, year=year)
			else:
				start_dt = None

		else:
			start_dt = None

		if end_date:
			date_split = end_date.split('/')

			if len(date_split) == 3:
				month,day,year = [int(x) for x in date_split]
				end_dt = datetime.date(day=day, month=month, year=year)
			else:
				end_dt = None

		else:
			end_dt = None

		job = Job(
			profile=profile,
			job_title=job_title,
			responsibility=responsibility,
			start_date=start_dt,
			end_date=end_dt,
			company_name=company_name,
			company_size=company_size,
			work_location=work_location)
		job.save()

		if currency:
			job.currency = currency

		if max_salary:
			job.max_salary = max_salary

		if min_salary:
			job.min_salary = min_salary

		if work_location:
			exists = Location.objects.filter(name=work_location)

			if not exists:
				new_location = Location(name=work_location)
				new_location.save()

		if job_type:
			job.job_type = job_type

		if education_level:
			job.education_level = education_level

		if personality:
			job.personality = personality

		if job_level:
			job.job_level = job_level

		if max_salary:
			job.max_salary = max_salary

		if min_salary:
			job.min_salary = min_salary

		if work_experience:
			job.work_experience = work_experience

		if contacts:
			job.contacts = contacts

		if training:
			job.training = training

		if institutions:
			if institutions == 'N/A':
				job.institution_not_needed = True

			else:
				is_list = type(institutions) == list

				if is_list:
					for institute in institutions:
						exists = Institute.objects.filter(name=institute)

						if exists:
							inst_db = exists[0]
						else:
							inst_db = Institute(name=institute)
							inst_db.save()

						job.institutions.add(inst_db)

				else:
					exists = Institute.objects.filter(name=institutions)

					if exists:
						inst_db = exists[0]
					else:
						inst_db = Institute(name=institute)
						inst_db.save()

					job.institutions.add(inst_db)

		if skills:
			is_list = type(skills) == list

			if is_list:
				for skill in skills:
					exists = Skill.objects.filter(name=skill)

					if exists:
						skill_db = exists[0]
					else:
						skill_db = Skill(name=skill)
						skill_db.save()

					job.skills.add(skill_db)

			else:
				exists = Skill.objects.filter(name=skills)

				if exists:
					skill_db = exists[0]
				else:
					skill_db = Skill(name=skill)
					skill_db.save()

				job.skills.add(skill_db)

		if hard_skills:
			is_list = type(skills) == list

			if is_list:
				for skill in hard_skills:
					exists = HardSkill.objects.filter(name=skill)

					if exists:
						skill_db = exists[0]
					else:
						skill_db = HardSkill(name=skill)
						skill_db.save()

					job.hard_skills.add(skill_db)

			else:
				exists = HardSkill.objects.filter(name=skills)

				if exists:
					skill_db = exists[0]
				else:
					skill_db = HardSkill(name=skill)
					skill_db.save()

				job.hard_skills.add(skill_db)

		if languages:
			if languages == "N/A":
				job.language_not_needed = True

			else:
				job.languages.clear()

				keys = languages.keys()

				for key in keys:
					exp = languages[key]
					language, reading_level, writing_level, verbal_level = exp['language'], exp['reading-level'], exp['writing-level'], exp['verbal-level']

					la_db = JobLanguage(name=language)

					if reading_level:
						la_db.reading_level = reading_level

					if writing_level:
						la_db.writing_level = writing_level

					if verbal_level:
						la_db.verbal_level = verbal_level

					data_exists = reading_level or writing_level or verbal_level and language

					if data_exists:
						la_db.save()
						job.languages.add(la_db)

		job.save()

		if profile.application_details == False:
			profile.application_details = True
			profile.save()
			
		return {'status': True, 'job-id': job.id}			
	except Exception, e:
		return {'status': False, 'error_type': repr(e)}


def unlink_social(request, post_data):
	try:
		social = post_data['social']

		if social == 'linkedin':
			result = SocialAccount.objects.filter(provider='linkedin_oauth2', user_id=request.user.id)
			provider = 'Linkedin'
			link = '/accounts/linkedin_oauth2/login/?process=connect'

		elif social == 'google':
			result = SocialAccount.objects.filter(provider='google', user_id=request.user.id)
			provider = 'Google'
			link = '/accounts/google/login/?process=connect'

		elif social == 'twitter':
			result = SocialAccount.objects.filter(provider='twitter', user_id=request.user.id)
			provider = 'Twitter'
			link = '/accounts/twitter/login/?process=connect'

		elif social == 'stackoverflow':
			result = SocialAccount.objects.filter(provider='stackexchange', user_id=request.user.id)
			provider = 'Stack Overflow'
			link = '/accounts/stackexchange/login/?process=connect'

		elif social == 'facebook':
			result = SocialAccount.objects.filter(provider='facebook', user_id=request.user.id)
			provider = 'Facebook'
			link = '/accounts/facebook/login/?process=connect'

		if result:
			for item in result:
				item.delete()

		text = 'Link {0}'.format(provider)

		return {'status': True, 'text': text, 'link': link}			
	except Exception, e:
		return {'status': False, 'error_type': repr(e)}


		

def update_user_profile(request):
	response = {'status': None}

	if request.method == 'POST':
		post_data = json.loads(request.body)

		
		if not request.user.is_authenticated():
			response['error_type'] = "Invalid Request"
		else:
			user_id = request.user.id
			user = User.objects.get(id=user_id)
			profile = user.profile.first()

			status_update = profile_update(profile, post_data)
			profile.auto_responder()

			if status_update['status'] == True:
				response['status'] = "OK"
			else:
				response['error_type'] = "Update Failed, if this occurs frequently please contact support for help. Error Message: {0}".format(status_update['error_type'])

	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def update_job_criteria(request):
	response = {'status': None}

	if request.method == 'POST':
		post_data = json.loads(request.body)

		if not request.user.is_authenticated():
			response['error_type'] = "Invalid Request"
		else:
			user_id = request.user.id
			user = User.objects.get(id=user_id)
			profile = user.profile.first()

			status_update = job_criteria_save(profile, post_data)

			if status_update['status'] == True:
				response['status'] = "OK"
			else:
				response['error_type'] = "Update Failed, if this occurs frequently please contact support for help. Error Message: {0}".format(status_update['error_type'])
 
	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def update_work_experience(request):
	response = {'status': None}

	if request.method == 'POST':
		post_data = json.loads(request.body)

		if not request.user.is_authenticated():
			response['error_type'] = "Invalid Request"
		else:
			user_id = request.user.id
			user = User.objects.get(id=user_id)
			profile = user.profile.first()

			status_update = work_experience_save(profile, post_data)

			if status_update['status'] == True:
				response['status'] = "OK"
			else:
				response['error_type'] = "Update Failed, if this occurs frequently please contact support for help. Error Message: {0}".format(status_update['error_type'])
 
	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def search_ajax(request):
	response = {'status': None, 'html': '', 'more': None, 'result': None}
	response['user-authenticated'] = request.user.is_authenticated()

	if request.method == 'POST':
		data = json.loads(request.body)
		search, search_type = data['search'], data['type']

		context = {}
		if search_type == 'Service':
			services = [x for x in Service.objects.filter(name__icontains=search, active=True) if x.no_active_providers() > 0]
			
			response['total'] = len(services)
			context['services'] = services[:10]
			response['more'] = len(services) > 10
			response['result'] = len(services) > 0
			response['html'] = render_to_string('snippets/search-result.html', context)

			context['services'] = services
			response['full-html'] = render_to_string('snippets/search-result.html', context)

		elif search_type == 'Job':
			jobs = [x for x in Job.objects.filter(Q(job_title__icontains=search) | Q(responsibility__icontains=search)) if x.check_status() == 'Active']

			response['total'] = len(jobs)
			context['jobs'] = jobs[:10]
			response['more'] = len(jobs) > 10
			response['result'] = len(jobs) > 0
			response['html'] = render_to_string('snippets/search-result.html', context)

			context['jobs'] = jobs
			response['full-html'] = render_to_string('snippets/search-result.html', context)


		elif search_type == 'Candidate by skill/name':
			skills = Skill.objects.filter(active=True, name__icontains=search)
			hard_skills = HardSkill.objects.filter(active=True, name__icontains=search)
			users = list(set(UserAccount.objects.filter(Q(user__is_active=True) & Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(skills__in=skills) | Q(hard_skills__in=hard_skills))))

			response['total'] = len(users)
			context['users'] = users[:10]
			response['more'] = len(users) > 10
			response['result'] = len(users) > 0
			context['admin'] = staff = request.user.is_staff
			response['html'] = render_to_string('snippets/search-result.html', context)

			context['users'] = users
			context['admin'] = staff
			response['full-html'] = render_to_string('snippets/search-result.html', context)

		response['status'] = 'ok'
	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def service_update(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body)
		search = data['search']

		if request.user.is_authenticated():
			email = request.user.email

			context = {'email': email}
			context['services'] = Service.objects.filter(name__icontains=search, active=True)
			
			html_body = render_to_string('emails/services.html', context)
			body = render_to_string('emails/services.txt', context)

			msg = EmailMultiAlternatives("KaziLynk Search Result: {0}".format(search), body, from_email, [email])
			msg.attach_alternative(html_body, "text/html")
			msg.send()

			response['status'] = 'ok'
		else:
			response['error_type'] = 'User not logged in'

	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def service_post(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body)
		email, search = data['email'], data['search']

		saved = ServiceAlert.objects.filter(email=email)

		if not saved:
			email_alert = ServiceAlert(email=email)
			email_alert.save()

		context = {}
		context['services'] = Service.objects.filter(name__icontains=search, active=True)
		
		html_body = render_to_string('emails/services.html', context)
		body = render_to_string('emails/services.txt', context)

		msg = EmailMultiAlternatives("KaziLynk Search Result: {0}".format(search), body, from_email, [email])
		msg.attach_alternative(html_body, "text/html")
		msg.send()

		response['status'] = 'ok'
	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def update_skill(request):
	response = {'status': None}

	if request.method == 'POST':
		post_data = json.loads(request.body)

		if not request.user.is_authenticated():
			response['error_type'] = "Invalid Request"
		else:
			user_id = request.user.id
			user = User.objects.get(id=user_id)
			profile = user.profile.first()

			status_update = skill_save(profile, post_data)

			if status_update['status'] == True:
				response['status'] = "OK"
			else:
				response['error_type'] = "Update Failed, if this occurs frequently please contact support for help. Error Message: {0}".format(status_update['error_type'])
 
	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def update_service(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body)
		company_name, negotiable, email, phone_no, website, location, service_txt, testimonial, charge, business_details, service_id, links, remove_links, prices, remove_prices = data['company-name'], data['rates-negotiable'], data['email'], data['phone-no'], data['company-website'], data['location'], data['service'], data['testimonial'], data['charge'], data['business-details'], data['service-id'], data['links'], data['remove-links'], data['prices'], data['remove-prices']
		
		profile = request.user.profile.first()

		exists = UserService.objects.filter(id=service_id, profile=profile)

		if exists:
			service = exists[0]

			if testimonial:
				service.testimonial = testimonial

			if charge:
				service.price = charge

			if business_details:
				service.business_details = business_details

			for key in links.keys():
				link = links[key]

				if 'new' in link['exp-id']:
					link_db = Link(link=link['link'], link_info=link['link-info'], profile=profile)
					link_db.save()

					service.links.add(link_db)

				else:
					link_db = Link.objects.get(id=link['exp-id'])

					if link_db in service.links.all(): #edit only for this
						link_db.link = link['link']
						link_db.link_info = link['link-info']
						link_db.save()

			for exp_id in remove_links:
				link_db = Link.objects.get(id=exp_id)

				if link_db in service.links.all():
					link_db.delete()

			for key in prices.keys():
				price = prices[key]

				if 'new' in price['exp-id']:
					price_db = Price(name=price['price'])
					price_db.save()

					service.prices.add(price_db)

				else:
					price_db = Price.objects.get(id=price['exp-id'])

					if price_db in service.prices.all():
						price_db.name = price['price']
						price_db.save()

			for exp_id in remove_prices:
				price_db = Price.objects.get(id=exp_id)

				if price_db in service.prices.all():
					price_db.delete()

			if company_name:
				service.company_name = company_name

			service.negotiable = negotiable

			if email:
				service.email = email

			if phone_no:	
				service.phone_no = phone_no

			if website:
				service.company_website = website

			if location:
				service.location = location

				exists = Location.objects.filter(name=location)

				if not exists:
					new_location = Location(name=location)
					new_location.save()

			if service_txt:
				exists = Service.objects.filter(name=service_txt)

				if exists:
					service_db = exists[0]

				else:
					service_db = Service(name=service)
					service_db.save()

				service.service = service_db

			service.save()

		else:
			response['error_type'] = "Service not found or user currently logged isn't the author"

	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def update_language(request):
	response = {'status': None}

	if request.method == 'POST':
		post_data = json.loads(request.body)

		if not request.user.is_authenticated():
			response['error_type'] = "Invalid Request"
		else:
			user_id = request.user.id
			user = User.objects.get(id=user_id)
			profile = user.profile.first()

			status_update = language_save(profile, post_data)

			if status_update['status'] == True:
				response['status'] = "OK"
			else:
				response['error_type'] = "Update Failed, if this occurs frequently please contact support for help. Error Message: {0}".format(status_update['error_type'])
 
	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def update_documents(request):
	response = {'status': None}

	if request.method == 'POST':
		post_data = json.loads(request.body)

		if not request.user.is_authenticated():
			response['error_type'] = "Invalid Request"
		else:
			user_id = request.user.id
			user = User.objects.get(id=user_id)
			profile = user.profile.first()

			link_update = links_save(profile, post_data)

			status_update = {}

			if link_update['status'] == True:
				status_update['status'] = True

			elif link_update['error_type'] :
				status_update['error_type'] = link_update['error_type']

			if status_update['status'] == True:
				response['status'] = "OK"
			else:
				response['error_type'] = "Update Failed, if this occurs frequently please contact support for help. Error Message: {0}".format(status_update['error_type'])
 
	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def update_employer(request):
	response = {'status': None}

	if request.method == 'POST':
		post_data = json.loads(request.body)

		if not request.user.is_authenticated():
			response['error_type'] = "Invalid Request"
		else:
			user_id = request.user.id
			user = User.objects.get(id=user_id)
			profile = user.profile.first()

			status_update = employer_save(profile, post_data)

			if status_update['status'] == True:
				response['status'] = "OK"
			else:
				response['error_type'] = "Update Failed, if this occurs frequently please contact support for help. Error Message: {0}".format(status_update['error_type'])
 
	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def update_job(request):
	response = {'status': None}

	if request.method == 'POST':
		post_data = json.loads(request.body)

		if not request.user.is_authenticated():
			response['error_type'] = "Invalid Request"
		else:
			user_id = request.user.id
			user = User.objects.get(id=user_id)
			profile = request.user.profile.first()

			status_update = job_save(profile, post_data)

			if status_update['status'] == True:
				response['status'] = "OK"
				response['redirect-url'] = reverse('view_job', kwargs={'job_id': status_update['job-id']})
			else:
				response['error_type'] = "Update Failed, if this occurs frequently please contact support for help. Error Message: {0}".format(status_update['error_type'])
 
	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)


def update_education(request):
	response = {'status': None}

	if request.method == 'POST':
		post_data = json.loads(request.body)

		if not request.user.is_authenticated():
			response['error_type'] = "Invalid Request"
		else:
			user_id = request.user.id
			user = User.objects.get(id=user_id)
			profile = user.profile.first()

			status_update = education_save(profile, post_data)

			if profile.education_incomplete():
				response['message'] = "Please Fill All Fields Highlighted"
			else:
				response['message'] = None

			if status_update['status'] == True:
				response['status'] = "OK"
			else:
				response['error_type'] = "Update Failed, if this occurs frequently please contact support for help. Error Message: {0}".format(status_update['error_type'])
 
	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def update_social(request):
	response = {'status': None}

	if request.method == 'POST':
		post_data = json.loads(request.body)

		if not request.user.is_authenticated():
			response['error_type'] = "Invalid Request"
		else:
			user_id = request.user.id
			user = User.objects.get(id=user_id)
			profile = user.profile.first()

			status_update = unlink_social(request, post_data)

			if status_update['status'] == True:
				response['status'] = "OK"
				response['text'] = status_update['text']
				response['link'] = status_update['link']

			else:
				response['error_type'] = "Update Failed, if this occurs frequently please contact support for help. Error Message: {0}".format(status_update['error_type'])
 
	else:
		response['error_type'] = 'No POST DATA Found'

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)


def update_profile(request):
	response = {'status': None}
	if request.method == 'POST':
		post_data = json.loads(request.body)

		first_name, last_name, country_code, heard_from, user_id, code = post_data['first_name'], post_data['last_name'], post_data['country'], post_data['heard-from'], post_data['user-id'], post_data['verification-code']
		other_source = post_data['other-source']

		if request.user.is_authenticated():
			user_id = request.user.id
			code = request.user.profile.first().email_verification_code

		user = User.objects.get(id=user_id)
		profile = user.profile.first()
		today = timezone.now()
		validation_key = profile.email_verification_code
		expiry = profile.email_validation_expire

		if other_source:
			heard_from = other_source

		profile.first_name = first_name
		profile.last_name = last_name

		profile.country = country_code
		profile.heard_from = heard_from
		
		profile.profile_complete = True
		profile.save()

		response['status'] = "OK"
		
	else:
		response['error_type'] = "No POST Data Found"

	return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)		

def create_user(request):
	response = {'status': None}
	if request.method == 'POST':
		post_data = json.loads(request.body)
		
		email, password, category, names = post_data['email'], post_data['password'], post_data['user_category'], post_data['names']
		email = email.lower()

		if category[-1] == 's':
			category = category[:-1] #remove 's' in Employer(s), Service Seeker(s) & Service Provider(s)

		try:
			new_user = user = User.objects.create_user(email, email, password)
			names_split = names.split(' ')

			if len(names_split) >= 2:
				new_user.first_name = names_split[0]
				new_user.last_name = names_split[1]
				first_name = names_split[0]
				last_name = names_split[1]
			else:
				new_user.first_name = names_split[0]
				first_name = names_split[0]
				last_name = ''

			new_user.is_active = False
			new_user.save()
			
			

			user_json = {'email': email}
			body = render_to_string('emails/new_user.txt', user_json)
			msg = EmailMessage('New User Created', body, from_email, regisration_admins)
			msg.send()

			profile = UserAccount(user=new_user, category=category, first_name=first_name, last_name=last_name)
			profile.save()


			domain = "http://"+request.get_host()
			confirmation_link = domain + reverse('confirmation_link', kwargs={'user_id': new_user.id, 'code': profile.email_verification_code})
			#confirmation_link = domain+'/register/account_completion/'+profile.email_verification_code+'?email='+email

			user_email = user_json['email']

			confirm_json = {'confirmation_link': confirmation_link, 'category': category}
			body = render_to_string('emails/confirm_user.txt', confirm_json)
			html_body = render_to_string('emails/confirm_user.html', confirm_json)

			recepients = regisration_admins[:]
			recepients.append(user_email)
			msg = EmailMultiAlternatives("KaziLynk: New User Created", body, from_email, recepients)
			msg.attach_alternative(html_body, "text/html")
			msg.send()

			response['status'] = "ok"
		except Exception, e:
			response['status'] = None
			response['error_type'] = repr(e)


		return HttpResponse(
				json.dumps(response),
				content_type="application/json"
			)
	else:
		response['error_type'] = 'No Post'
		return HttpResponse(
				json.dumps(response),
				content_type="application/json"
			)

def email_checkup_json(request):
	response = {}
	if request.method == 'GET':
		email = request.GET.get('email', None)
		email = email.lower()

		if email:
			exists = User.objects.filter(email=email)
			response['exists'] = bool(exists)
			response['error'] = False

		else:
			response['exists'] = None
			response['error'] = True
			response['error_message'] = 'Email Not Found'

	else:
		response['exists'] = None
		response['error'] = True
		response['error_message'] = 'No JSON Object Found'

	return HttpResponse(
                    json.dumps(response),
                    content_type="application/json"
                )


def signup(request, template_name="accounts/signup.html"):
	context = RequestContext(request)
	profile_cat = request.GET.get('cat', None)

	if not profile_cat:
		return redirect('/register')

	context['profile_cat'] = profile_cat.replace('_',' ').title()

	return render_to_response(template_name, context)