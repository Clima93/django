from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.models import UserAccount
from sorl.thumbnail import get_thumbnail
from django.core.urlresolvers import reverse
import string

#from mailchimp3 import MailChimp

class ServiceAlert(models.Model):
	email = models.CharField(max_length=100, unique=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.email

class NewsLetterEmail(models.Model):
	email = models.CharField(unique=True, max_length=100)
	active = models.BooleanField(default=True)
	registered = models.BooleanField(default=False)

	def __unicode__(self):
		return self.email

	def mailchimp_register(self):
		client = MailChimp('damaris@kazilynk.com', 'b990a6b6b3566d06b317c39c9d89ecd3-us16')

		try:
			client.lists.members.create('100e27ae73', {
			    'email_address': self.user.email,
			    'status': 'subscribed',
			    'merge_fields': {
			        'FNAME': self.first_name,
			        'LNAME': self.last_name,
			    },
			})

		except:
			pass

		self.registered = True
		self.save()

	def save(self, *args, **kwargs):
		if not self.registered:
			self.mailchimp_register()

		return super(NewsLetterEmail, self).save(*args, **kwargs)

class Article(models.Model):
	title = models.CharField(max_length=500)
	description = models.TextField(null=True)
	image = models.ImageField(upload_to='uploads', max_length=500, null=True)
	sub_title = models.CharField(max_length=500, blank=True)
	html = RichTextUploadingField()
	author = models.CharField(max_length=100, blank=True, null=True)
	active = models.BooleanField(default=True)
	on_homepage = models.BooleanField(default=False)
	popular = models.BooleanField(default=False)
	top_article = models.BooleanField(default=False)
	slug = models.SlugField(unique=True, blank=True, null=True)

	def __unicode__(self):
		return self.title

	def slug_text(self):
		return self.slug.replace(' ','-')

	def get_thumbnail(self):
		if not self.image:
			return ''

		im = get_thumbnail(self.image, '356x260', crop="top", quality=100)
		return im.url

	def get_valid_slug(self, valid_text):
		new_slug = ''
		for char in self.slug:
			if char in valid_text:
				new_slug += char

		return new_slug

	def url(self):
		return reverse('view_article', kwargs={'slug': self.slug_text})

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self.title.lower()

		valid_text = string.lowercase + string.uppercase + string.digits + ' '

		valid_slug = True
		for char in self.slug:
			if char not in valid_text:
				valid_slug = False
				break

		if valid_slug == False:
			self.slug = self.get_valid_slug(valid_text)			

		return super(Article, self).save(*args, **kwargs)

class Quote(models.Model):
	text = models.TextField()
	author = models.CharField(max_length=500, blank=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return "{0} - {1}".format(self.text, self.author)

class Location(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	parent = models.CharField(max_length=100, null=True, blank=True)
	active = models.BooleanField(default=False)

	country = models.BooleanField(default=False)
	country_name = models.CharField(max_length=100, null=True, blank=True)
	country_code = models.CharField(max_length=10, null=True, blank=True)

	def __unicode__(self):
		return "{0} {1} - {2}".format(self.name, self.country, self.country_code)
			