"""
Django settings for repository project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = BASE_DIR
# MEDIA_ROOT = os.path.join(os.path.abspath("."))

from django.utils.translation import ugettext_lazy as _

from t47_dev import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = T47_DEV
TEMPLATE_DEBUG = DEBUG

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/site_data/'
STATIC_ROOT = ''
if os.path.exists('/home/ubuntu/Files/'):
    STATICFILES_DIRS = ('/home/ubuntu/Files/', )
else:
    STATICFILES_DIRS = (MEDIA_ROOT + '/files/', )
ADMIN_MEDIA_PREFIX = '/admin/'

ADMINS = (
    ('Siqi Tian', 't47@stanford.edu'),
    # ('Pablo Cordero', 'tsuname@stanford.edu'),
)
MANAGERS = ADMINS
EMAIL_NOTIFY = ADMINS[0][1]
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'stanfordrmdb@gmail.com'
EMAIL_HOST_PASSWORD = 'daslab4ever'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.humanize',

    'src',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",

)
gettext = lambda s: s
CMS_TEMPLATES = (
    ('default.html', gettext('default')),
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_DIRS = (
    MEDIA_ROOT,
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

ROOT_URLCONF = 'src.urls'
WSGI_APPLICATION = 'src.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'daslab',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'beckman',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
LOGIN_URL = '/login'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('en', _('English')),
)
SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"

class SYS_PATH:
    def __init__(self):
        self.HTML_PATH = {
            'index': MEDIA_ROOT + '/media/html/index.html',
            'research': MEDIA_ROOT + '/media/html/research.html',
            'news': MEDIA_ROOT + '/media/html/news.html',
            'people': MEDIA_ROOT + '/media/html/people.html',
            'publications': MEDIA_ROOT + '/media/html/publications.html',
            'resources': MEDIA_ROOT + '/media/html/resources.html',
            'contact': MEDIA_ROOT + '/media/html/contact.html',

            'login': MEDIA_ROOT + '/media/html/_login.html',
            'password': MEDIA_ROOT + '/media/html/_password.html',

            'lab_meetings': MEDIA_ROOT + '/media/html/lab_meetings.html',
            'lab_calendar': MEDIA_ROOT + '/media/html/lab_calendar.html',
            'lab_resources': MEDIA_ROOT + '/media/html/lab_resources.html',
            'lab_misc': MEDIA_ROOT + '/media/html/lab_misc.html',

            '404': MEDIA_ROOT + '/media/html/_404.html',
            '500': MEDIA_ROOT + '/media/html/_500.html',
        }

        self.DATA_DIR = {
            'MEMBER_IMG_DIR': STATICFILES_DIRS[0] + '/ppl_img/',
            'PUB_PDF_DIR': STATICFILES_DIRS[0] + '/pub_pdf/',
            'PUB_IMG_DIR': STATICFILES_DIRS[0] + '/pub_img/',
            'PUB_DAT_DIR': STATICFILES_DIRS[0] + '/pub_data/',
            'NEWS_IMG_DIR': STATICFILES_DIRS[0] + '/news_img/',

            'ROT_PPT_DIR': STATICFILES_DIRS[0] + '/rot_ppt/',
            'ROT_DAT_DIR': STATICFILES_DIRS[0] + '/rot_data/',
            'SPE_PPT_DIR': STATICFILES_DIRS[0] + '/spe_ppt/',

            'TMPDIR': MEDIA_ROOT + '/temp/',

        }
PATH = SYS_PATH()


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!9g7%50idfw-=(ii6mr3kmt@a*&-b%32q^!a!tkrwt%%+p^iu#'

