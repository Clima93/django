"""
Django settings for kazilynk project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#-w+7)c&#r+oh(7n0t#39*0i*tmpmki$66y%ty0^f4g@mdnjua'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

EMAIL_HOST = 'mail.kazilynk.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@kazilynk.com'
EMAIL_HOST_PASSWORD = "s8YnZ2SWKpUv2cXk"
EMAIL_USE_TLS = True

DEFAULT_EMAIL = 'no-reply@kazilynk.com'
SERVER_EMAIL = 'no-reply@kazilynk.com'
DEFAULT_FROM_EMAIL = 'no-reply@kazilynk.com'
DEFAULT_TO_EMAIL = 'website@kazilynk.com'
DEFAULT_FROM_EMAIL_NAME = 'KaziLynk'
DEFAULT_TO_EMAIL_NAME = 'KaziLynk'

#Set to False for No Expiry
EMAIL_EXPIRY_DAYS = 5

#DJango Oauth
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_REQUIRED = True
#ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_USERNAME_REQUIRED = False
LOGIN_REDIRECT_URL = '/accounts/profile'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "KaziLynk: "

# Application definition

INSTALLED_APPS = (
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin_oauth2',
    #'allauth.socialaccount.providers.paypal',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.stackexchange',

    'django_countries',
    'fontawesome',

    'accounts',
    'common',
    'pages',
)

SITE_ID = 1

CONTACT_ADMINS = REGISTRATION_ADMINS = ['support@kazilynk.com', 'damaris@kazilynk.com']

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'kazilynk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'kazilynk/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kazilynk.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kazilynk',
        'USER': 'overload',
        'PASSWORD': 'eastood0009',
        'HOST': 'localhost',
        'PORT': '',
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



UPLOAD_DIR = MEDIA_ROOT+'/uploads'
CKEDITOR_UPLOAD_PATH = 'uploads/'
