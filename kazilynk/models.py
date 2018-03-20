from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
EMAIL_EXPIRY_DAYS, SECRET_KEY = settings.EMAIL_EXPIRY_DAYS, settings.SECRET_KEY
import hashlib
from django_countries.fields import CountryField
from django.utils import timezone
from allauth.socialaccount.models import SocialAccount
from common.tools import calendar_date_to_datetime as date_conv
from sorl.thumbnail import get_thumbnail
from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from jet.utils import LazyDateTimeEncoder
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class UserDashboardModule(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    module = models.CharField(verbose_name=_('module'), max_length=255)
    app_label = models.CharField(verbose_name=_('application name'), max_length=255, null=True, blank=True)
    user = models.PositiveIntegerField(verbose_name=_('user'))
    column = models.PositiveIntegerField(verbose_name=_('column'))
    order = models.IntegerField(verbose_name=_('order'))
    settings = models.TextField(verbose_name=_('settings'), default='', blank=True)
    children = models.TextField(verbose_name=_('children'), default='', blank=True)
    collapsed = models.BooleanField(verbose_name=_('collapsed'), default=False)

    class Meta:
        verbose_name = _('user dashboard module')
        verbose_name_plural = _('user dashboard modules')
        ordering = ('column', 'order')

    def __str__(self):
        return self.module

    def load_module(self):
        try:
            package, module_name = self.module.rsplit('.', 1)
            package = import_module(package)
            module = getattr(package, module_name)

            return module
        except AttributeError:
            return None
        except ImportError:
            return None

    def pop_settings(self, pop_settings):
        settings = json.loads(self.settings)

        for setting in pop_settings:
            if setting in settings:
                settings.pop(setting)

        self.settings = json.dumps(settings, cls=LazyDateTimeEncoder)
        self.save()

    def update_settings(self, update_settings):
        settings = json.loads(self.settings)

        settings.update(update_settings)

        self.settings = json.dumps(settings, cls=LazyDateTimeEncoder)
        self.save()




#django jet module admin
class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            10,
            column=0,
            order=0
        ))

#django jet module admin
class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.children.append(modules.Feed(
            _('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5,
            column=0,
            order=0
        ))

class Link(models.Model):
	link = models.CharField(max_length=1000)
	link_info = models.TextField()
	active = models.BooleanField(default=True)
	profile = models.ForeignKey('UserAccount', related_name="links")

	def __unicode__(self):
		return self.link

class UserLanguage(models.Model):
	language = models.CharField(max_length=500, null=True)
	active = models.BooleanField(default=True)
	verbal_level = models.CharField(max_length=100, blank=True)
	writing_level = models.CharField(max_length=100, blank=True)
	reading_level = models.CharField(max_length=100, blank=True)
	profile = models.ForeignKey('UserAccount', related_name="languages", null=True)

	def __unicode__(self):
		return self.language

	def complete(self):
		all_filled = bool(self.language and self.verbal_level and self.writing_level and self.reading_level)

		return all_filled

class HardSkill(models.Model):
	name = models.CharField(max_length=500, unique=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.name

class Skill(models.Model):
	name = models.CharField(max_length=500, unique=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.name

class Institute(models.Model):
	name = models.CharField(max_length=300, blank=True, null=True, unique=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.name


class Education(models.Model):
	institute = models.ForeignKey('Institute', blank=True, null=True)
	level = models.CharField(max_length=300, blank=True, null=True)
	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)
	profile = models.ForeignKey('UserAccount', blank=True, null=True, related_name='education')
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return "{0}".format(self.level)

	def end_date_str(self):
		if self.end_date:
			return self.end_date.strftime("%d/%m/%Y")
		else:
			return "Current"	

class WorkExperience(models.Model):
	company_name = models.CharField(max_length=300, blank=True, null=True)
	employer_name = models.CharField(max_length=300, blank=True, null=True)
	job_title = models.CharField(max_length=300, blank=True, null=True)
	responsibility = models.TextField(blank=True, null=True)
	achievements = models.TextField(blank=True, null=True)
	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)
	profile = models.ForeignKey('UserAccount', blank=True, null=True, related_name='experience')
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return "{0}".format(self.company_name)

	def end_date_str(self):
		if self.end_date:
			return self.end_date.strftime("%d/%m/%Y")
		else:
			return "Current"

class WorkIndustry(models.Model):
	delay_in_hrs = 2

	seconds_value = delay_in_hrs * 3600
	set_time = timezone.now() + datetime.timedelta(seconds=seconds_value)

	name = models.CharField(max_length=250, unique=True)
	active = models.BooleanField(default=True)
	verification_code = models.CharField(max_length=250, blank=True)
	start_time = models.DateTimeField(default=set_time)
	#activate = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

	def visible(self):
		if self.active and timezone.now() > self.start_time:
			return True

		return False

	def save(self, *args, **kwargs):
		if not self.verification_code:
			key = hashlib.new("ripemd160")
			key.update(self.name + SECRET_KEY)
			key_string = key.hexdigest()

			self.verification_code = key_string

		return super(WorkIndustry, self).save(*args, **kwargs)

class Industry(models.Model):
	name = models.CharField(max_length=500, unique=True)

	def __unicode__(self):
		return "{0}".format(self.name)

class Language(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class JobLanguage(models.Model):
	name = models.CharField(max_length=250)
	reading_level = models.CharField(max_length=100, blank=True)
	writing_level = models.CharField(max_length=100, blank=True)
	verbal_level = models.CharField(max_length=100, blank=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.name

class Personality(models.Model):
	name = models.CharField(max_length=250)

	def __unicode__(self):
		return self.name
		
class Job(models.Model):
	profile = models.ForeignKey('UserAccount', related_name='jobs')
	job_title = models.CharField(max_length=500)
	responsibility = models.TextField(blank=True)
	job_type = models.CharField(max_length=100, blank=True)
	min_salary = models.CharField(max_length=500, blank=True)
	max_salary = models.CharField(max_length=500, blank=True)
	job_level = models.CharField(max_length=100, blank=True)
	start_date = models.DateField(max_length=100, blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)
	industry = models.CharField(max_length=500, null=True, blank=True)
	department = models.CharField(max_length=500, null=True, blank=True)
	active = models.BooleanField(default=True)

	work_location = models.CharField(max_length=500, null=True, blank=True)
	created_on = models.DateTimeField(default=datetime.datetime.now, null=True)
	education_level = models.CharField(max_length=100, null=True, blank=True)
	institutions = models.ManyToManyField(Institute, blank=True)
	institution_not_needed = models.BooleanField(default=False)
	training = models.CharField(max_length=500, null=True, blank=True)
	work_experience = models.TextField(null=True, blank=True)
	skills = models.ManyToManyField(Skill, blank=True)
	hard_skills = models.ManyToManyField(HardSkill, blank=True)
	skill_not_needed = models.BooleanField(default=False)
	languages = models.ManyToManyField(JobLanguage, blank=True)
	language_not_needed = models.BooleanField(default=False)
	personality = models.TextField(blank=True, null=True)
	contacts = models.CharField(max_length=500, blank=True, null=True)
	sex = models.CharField(max_length=20, blank=True, null=True)
	age = models.CharField(max_length=20, blank=True, null=True)
	viewers = models.ManyToManyField(User, blank=True)
	company_name = models.CharField(max_length=500, blank=True, null=True)
	company_size = models.CharField(max_length=500, blank=True, null=True)

	def __unicode__(self):
		return "{0}".format(self.job_title)

	def views(self):
		if not self.viewers.all():
			return 0

		return len(self.viewers.all())

	def start_date_str(self):
		if not self.start_date:
			return ''

		return self.start_date.strftime('%m/%d/%Y')

	def end_date_str(self):
		if not self.end_date:
			return ''

		return self.end_date.strftime('%m/%d/%Y')

	def job_matches(self):
		return 0

	def check_status(self):
		now = datetime.date.today()
		if self.active and self.end_date > now or self.end_date == now:
			return "Active"

		return "Expired"

	def status_class(self):
		now = datetime.date.today()
		if self.active and self.end_date > now or self.end_date == now:
			return "green"

		return "error-message"

	def expired(self):
		if not self.end_date:
			return False

		now = datetime.date.today()

		if now > self.end_date:
			return True

		return False

	def applicants_found(self):
		return 0

	def applicants_matched(self):
		return 0

	def save(self, *args, **kwargs):
		if not self.end_date:
			self.end_date = datetime.date.today() + datetime.timedelta(days=14)

		super(Job, self).save(*args, **kwargs)

class Service(models.Model):
	name = models.CharField(max_length=500)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.name

	def no_active_providers(self):
		if not self.users.all():
			return 0

		return len(self.users.filter(active=True))


class UserService(models.Model):
	service = models.ForeignKey(Service, related_name="users")
	negotiable = models.BooleanField()
	company_name = models.CharField(max_length=500)
	email = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)
	company_website = models.CharField(max_length=500, blank=True)
	location = models.CharField(max_length=200)
	testimonial = models.CharField(max_length=1000, blank=True)
	price = models.CharField(max_length=500)
	business_details = models.CharField(max_length=1000)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return "{0} {1}".format(self.service.name, self.company_name)


class UserAccount(models.Model):
	if EMAIL_EXPIRY_DAYS:
		expire_date = datetime.datetime.today() + datetime.timedelta(EMAIL_EXPIRY_DAYS)
	else:
		expire_date = datetime.datetime.today() + datetime.timedelta(1000)

	CATEGORY = (
			('Job Seeker','Job Seeker'),
			('Employer','Employer'),
			('Service Seeker','Service Seeker'),
			('Service Provider','Service Provider'),
		)

	GENDER = (
			('Male','Male'),
			('Female','Female'),
		)

	user = models.ForeignKey(User, related_name="profile")
	image = models.ImageField(blank=True, upload_to="profile_upload", max_length=500)
	company_logo = models.ImageField(blank=True, upload_to="company_logo", max_length=500)
	services = models.ManyToManyField(UserService, blank=True)
	email_verification_code = models.CharField(max_length=250, blank=True)
	email_validation_expire = models.DateTimeField(default=expire_date)
	first_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50, blank=True)
	d_o_b = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)
	category = models.CharField(max_length=50, choices=CATEGORY, null=True, blank=True)
	work_industry = models.CharField(max_length=250, null=True, blank=True)
	created_on = models.DateTimeField(default=datetime.datetime.now)
	profile_complete = models.BooleanField(default=False)
	country = models.CharField(max_length=100, null=True, blank=True)
	heard_from = models.CharField(max_length=500, null=True, blank=True)
	phone = models.CharField(max_length=25, null=True, blank=True)
	phone_code = models.CharField(max_length=5, null=True, blank=True)

	personal_statement = models.TextField(null=True, blank=True)
	industry = models.ManyToManyField(Industry, blank=True)
	company_size = models.CharField(max_length=300, null=True, blank=True)
	company_name = models.CharField(max_length=500, null=True, blank=True)
	department = models.CharField(max_length=300, null=True, blank=True)
	work_location = CountryField(blank_label='Select Work Location', null=True, blank=True)
	job_level = models.CharField(max_length=100, blank=True, null=True)
	availability = models.CharField(max_length=100, blank=True, null=True)
	salary = models.CharField(max_length=100, blank=True, null=True)

	skills = models.ManyToManyField(Skill, blank=True)
	hard_skills = models.ManyToManyField(HardSkill, blank=True)

	employer_industry = models.CharField(max_length=500, null=True, blank=True)
	department = models.CharField(max_length=500, null=True, blank=True)
	application_details = models.BooleanField(default=False)
	document = models.FileField(upload_to="documents", max_length=500, null=True, blank=True)

	def __unicode__(self):
		return "{0} {1} {2}".format(self.first_name, self.last_name, self.user.email)

	def jobs_counter(self):
		jobs = [x for x in self.jobs.filter(active=True) if x.expired() == False]
		return len(jobs)

	def company_logo_thumb(self):
		if not self.company_logo:
			return None

		im = get_thumbnail(self.company_logo, '125x125', quality=100)

		return im.url

	def language_incomplete(self):
		if self.languages:
			states = [x.complete() for x in self.languages.filter(active=True)]
			if False in states:
				return True

		return False

	def profile_photo_thumb(self):
		if not self.image:
			return None

		im = get_thumbnail(self.image, '150x300', quality=100)

		return im.url

	def google_check(self):
		exists = SocialAccount.objects.filter(provider='google', user_id=self.user.id)

		if exists:
			return True

		return False

	def twitter_check(self):
		exists = SocialAccount.objects.filter(provider='twitter', user_id=self.user.id)

		if exists:
			return True

		return False

	def facebook_check(self):
		exists = SocialAccount.objects.filter(provider='facebook', user_id=self.user.id)

		if exists:
			return True

		return False

	def has_job_post(self):
		return bool(self.jobs.filter(active=True))


	def stackoverflow_check(self):
		exists = SocialAccount.objects.filter(provider='stackexchange', user_id=self.user.id)

		if exists:
			return True

		return False

	def linkedin_check(self):
		exists = SocialAccount.objects.filter(provider='linkedin_oauth2', user_id=self.user.id)

		if exists:
			return True

		return False

	def social_ratio(self):
		count = 0
		total = 5

		if self.google_check():
			count += 1

		if self.twitter_check():
			count += 1

		if self.facebook_check():
			count += 1

		if self.stackoverflow_check():
			count += 1

		if self.linkedin_check():
			count += 1

		return "{0}/{1}".format(count, total)


	def language_complete(self):
		if self.languages:
			states = [x.complete() for x in self.languages.filter(active=True)]
			if False in states:
				return False
			elif states:
				return True
		return False

	def skills_info(self):
		if self.skills:
			return ' , '.join([x.name for x in self.skills.all()])
		else:
			return None


	def hard_skills_info(self):
		if self.hard_skills:
			return ' , '.join([x.name for x in self.hard_skills.all()])
		else:
			return None

	def skills_exist(self):
		if self.skills.all():
			return len(self.skills.all())
		return ''

	def hard_skills_exist(self):
		if self.hard_skills.all():
			return len(self.hard_skills.all())
		return ''

	def complete_class(self):
		percent = self.complete()

		if percent <= 20:
			return "progress-bar-danger"
		elif percent <= 50:
			return "progress-bar-warning"
		else:
			return "progress-bar-success"

	def complete(self):
		count = 0
		total = 6

		if self.personal_details_complete():
			count += 1

		if self.job_criteria_complete():
			count += 1

		if self.work_experience_complete():
			count += 1

		if self.education_complete():
			count += 1

		if self.skills_complete():
			count += 1

		if self.language_complete():
			count += 1

		complete_ratio = float(count)/total
		complete_percentage = 10 + (complete_ratio * 90)

		return int(complete_percentage)


	def job_criteria_complete(self):
		all_filled = self.job_level and self.availability

		return all_filled

	def personal_details_complete(self):
		all_filled = self.first_name and self.last_name and self.gender and self.phone and self.country and self.d_o_b

		return all_filled

	def work_experience_complete(self):
		return bool(self.experience.filter(active=True))

	def education_incomplete(self):
		education = self.education.filter(active=True)

		if education:
			for item in education:
				data_filled = item.institute and item.level and item.start_date
				if not data_filled:
					return True

		return False

	def education_complete(self):
		education = self.education.filter(active=True)

		if education:
			for item in education:
				data_filled = item.institute and item.level and item.start_date
				if not data_filled:
					return False

			return True
		else:
			return False

	def skills_complete(self):
		all_filled = bool(self.skills.filter(active=True)) and bool(self.hard_skills.filter(active=True))

		return all_filled

	def save(self, *args, **kwargs):
		has_jobs = len(self.jobs.filter(active=True))
		had_jobs = len(self.jobs.all())

		if not self.email_verification_code:
			key = hashlib.new("ripemd160")
			key.update(self.user.email + SECRET_KEY)
			key_string = key.hexdigest()

			self.email_verification_code = key_string

		super(UserAccount, self).save(*args, **kwargs)


