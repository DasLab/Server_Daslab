from django.shortcuts import render

import environ
import os
import simplejson

from config.t47_dev import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = IS_DEVEL


def reload_conf(DEBUG, MEDIA_ROOT):
    env = environ.Env(DEBUG=DEBUG,)  # set default values and casting
    environ.Env.read_env('%s/config/env.conf' % MEDIA_ROOT)  # reading .env file

    env_oauth = simplejson.load(open('%s/config/oauth.conf' % MEDIA_ROOT))
    AWS = env_oauth['AWS']
    GA = env_oauth['GA']
    GCAL = env_oauth['CALENDAR']
    DRIVE = env_oauth['DRIVE']
    GIT = env_oauth['GIT']
    SLACK = env_oauth['SLACK']
    SLACK['ADMIN_NAME'] = '@' + SLACK['ADMIN_NAME']
    DROPBOX = env_oauth['DROPBOX']
    APACHE_ROOT = '/var/www'

    env_cron = simplejson.load(open('%s/config/cron.conf' % MEDIA_ROOT))
    CRONJOBS = env_cron['CRONJOBS']
    CRONTAB_LOCK_JOBS = env_cron['CRONTAB_LOCK_JOBS']
    KEEP_BACKUP = env_cron['KEEP_BACKUP']

    env_bot = simplejson.load(open('%s/config/bot.conf' % MEDIA_ROOT))
    BOT = env_bot
    IS_SLACK = env_bot['SLACK']['IS_SLACK']

    return (env, AWS, GA, GCAL, DRIVE, GIT, SLACK, DROPBOX, APACHE_ROOT, CRONJOBS, CRONTAB_LOCK_JOBS, KEEP_BACKUP, BOT, IS_SLACK)


class Singleton(object):
    '''Base class for singleton pattern
    '''

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class SYS_PATH(Singleton):
    def __init__(self, MEDIA_ROOT):
        self.HTML_PATH = {
            'index': MEDIA_ROOT + '/media/html/public_index.html',
            'research': MEDIA_ROOT + '/media/html/public_research.html',
            'news': MEDIA_ROOT + '/media/html/public_news.html',
            'people': MEDIA_ROOT + '/media/html/public_people.html',
            'publications': MEDIA_ROOT + '/media/html/public_publications.html',
            'resources': MEDIA_ROOT + '/media/html/public_resources.html',
            'contact': MEDIA_ROOT + '/media/html/public_contact.html',

            'login': MEDIA_ROOT + '/media/html/_login.html',
            'password': MEDIA_ROOT + '/media/html/group_password.html',
            'upload': MEDIA_ROOT + '/media/html/group_resource_upload.html',
            # 'profile': MEDIA_ROOT + '/media/html/group_profile.html',

            'group_index': MEDIA_ROOT + '/media/html/group_index.html',
            'group_pages': MEDIA_ROOT + '/media/html/group_xxx.html',

            'admin_apache': MEDIA_ROOT + '/media/html/admin_apache.html',
            'admin_aws': MEDIA_ROOT + '/media/html/admin_aws.html',
            'admin_ga': MEDIA_ROOT + '/media/html/admin_ga.html',
            'admin_bot': MEDIA_ROOT + '/media/html/admin_bot.html',
            'admin_git': MEDIA_ROOT + '/media/html/admin_git.html',
            'admin_backup': MEDIA_ROOT + '/media/html/admin_backup.html',
            'admin_dir': MEDIA_ROOT + '/media/html/admin_dir.html',
            'admin_man': MEDIA_ROOT + '/media/html/admin_man.html',
            'admin_ref': MEDIA_ROOT + '/media/html/admin_ref.html',
            'admin_secret': MEDIA_ROOT + '/media/html/admin_key.html',
            'admin_export': MEDIA_ROOT + '/media/html/admin_export.html',

            '400': MEDIA_ROOT + '/media/html/error_400.html',
            '401': MEDIA_ROOT + '/media/html/error_401.html',
            '403': MEDIA_ROOT + '/media/html/error_403.html',
            '404': MEDIA_ROOT + '/media/html/error_404.html',
            '500': MEDIA_ROOT + '/media/html/error_500.html',
            '503': MEDIA_ROOT + '/media/html/error_503.html',
        }

        self.DATA_DIR = {
            'MEMBER_IMG_DIR': MEDIA_ROOT + '/data/ppl_img/',
            'PUB_PDF_DIR': MEDIA_ROOT + '/data/pub_pdf/',
            'PUB_IMG_DIR': MEDIA_ROOT + '/data/pub_img/',
            'PUB_DAT_DIR': MEDIA_ROOT + '/data/pub_data/',
            'NEWS_IMG_DIR': MEDIA_ROOT + '/data/news_img/',

            'ROT_PPT_DIR': MEDIA_ROOT + '/data/rot_ppt/',
            'ROT_DAT_DIR': MEDIA_ROOT + '/data/rot_data/',
            'SPE_PPT_DIR': MEDIA_ROOT + '/data/spe_ppt/',
            'DEF_IMG_DIR': MEDIA_ROOT + '/data/def_img/',

            'TMPDIR': MEDIA_ROOT + '/temp/',
        }

        self.GROUP_PATH = {
            'meeting': ['schedule', 'flash_slide', 'journal_club', 'eterna_youtube', 'rotation'],
            'calendar': ['calendar'],
            'resource': ['gdocs', 'archive', 'archive/upload', 'defense', 'contact'],
            'service': ['bot', 'secret', 'git', 'slack', 'dropbox'],
            'server': ['aws', 'ga'],
            'misc': ['misc', 'error']
        }

        self.COLOR = ('brown', 'dark-red', 'danger', 'orange', 'warning', 'green', 'success', 'light-blue', 'info', 'primary', 'dark-blue', 'violet')
        self.PALETTE = {
            'orange': 'ff912e',
            'pink': 'ff69bc',
            'violet': 'c28fdd',
            'blue': '5496d7',
            'cyan': '439fe0',
            'yellow': 'ffc107',
            'green': '5ed400',
            'red': 'f44336',
        }


root = environ.Path(os.path.dirname(os.path.dirname(__file__)))
MEDIA_ROOT = root()
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: '/home/media/media.lawrence.com/'
PATH = SYS_PATH(MEDIA_ROOT)
# MEDIA_ROOT = os.path.join(os.path.abspath('.'))
FILEMANAGER_STATIC_ROOT = root('media/admin') + '/'

(env, AWS, GA, GCAL, DRIVE, GIT, SLACK, DROPBOX, APACHE_ROOT, CRONJOBS, CRONTAB_LOCK_JOBS, KEEP_BACKUP, BOT, IS_SLACK) = reload_conf(DEBUG, MEDIA_ROOT)



def error400(request, status=True):
    status = (request.GET['status'].lower() != 'false') if 'status' in request.GET else status
    status = 400 if status else 200
    return render(request, PATH.HTML_PATH['400'], status=status)

def error401(request, status=True):
    status = (request.GET['status'].lower() != 'false') if 'status' in request.GET else status
    status = 401 if status else 200
    return render(request, PATH.HTML_PATH['401'], status=status)

def error403(request, status=True, reason=''):
    status = (request.GET['status'].lower() != 'false') if 'status' in request.GET else status
    status = 403 if status else 200
    return render(request, PATH.HTML_PATH['403'], status=status)

def error404(request, status=True):
    status = (request.GET['status'].lower() != 'false') if 'status' in request.GET else status
    status = 404 if status else 200
    return render(request, PATH.HTML_PATH['404'], status=status)

def error500(request, status=True):
    status = (request.GET['status'].lower() != 'false') if 'status' in request.GET else status
    status = 500 if status else 200
    return render(request, PATH.HTML_PATH['500'], status=status)

def error503(request, status=True):
    status = (request.GET['status'].lower() != 'false') if 'status' in request.GET else status
    status = 503 if status else 200
    return render(request, PATH.HTML_PATH['503'], status=status)

