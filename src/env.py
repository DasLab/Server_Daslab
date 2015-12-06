import environ
import simplejson


def reload_conf(DEBUG, MEDIA_ROOT):
    env = environ.Env(DEBUG=DEBUG,) # set default values and casting
    environ.Env.read_env('%s/config/env.conf' % MEDIA_ROOT) # reading .env file

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

    return (env, AWS, GA, GCAL, DRIVE, GIT, SLACK, DROPBOX, APACHE_ROOT, CRONJOBS, CRONTAB_LOCK_JOBS, KEEP_BACKUP)


class SYS_PATH(object):
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

            'lab_home': MEDIA_ROOT + '/media/html/group_index.html',
            'lab_meeting_schedule': MEDIA_ROOT + '/media/html/group_meeting_schedule.html',
            'lab_meeting_flash': MEDIA_ROOT + '/media/html/group_meeting_flash.html',
            'lab_meeting_jc': MEDIA_ROOT + '/media/html/group_meeting_jc.html',
            'lab_meeting_eterna': MEDIA_ROOT + '/media/html/group_meeting_eterna.html',
            'lab_meeting_rotation': MEDIA_ROOT + '/media/html/group_meeting_rotation.html',
            'lab_calendar': MEDIA_ROOT + '/media/html/group_calendar.html',
            'lab_resource_gdocs': MEDIA_ROOT + '/media/html/group_resource_document.html',
            'lab_resource_archive': MEDIA_ROOT + '/media/html/group_resource_archive.html',
            'lab_resource_contact': MEDIA_ROOT + '/media/html/group_resource_contact.html',
            'lab_server_aws': MEDIA_ROOT + '/media/html/group_server_aws.html',
            'lab_server_ga': MEDIA_ROOT + '/media/html/group_server_ga.html',
            'lab_service_git': MEDIA_ROOT + '/media/html/group_service_git.html',
            'lab_service_slack': MEDIA_ROOT + '/media/html/group_service_slack.html',
            'lab_service_dropbox': MEDIA_ROOT + '/media/html/group_service_dropbox.html',
            'lab_misc': MEDIA_ROOT + '/media/html/group_misc.html',
            'lab_error': MEDIA_ROOT + '/media/html/group_error.html',

            'admin_apache': MEDIA_ROOT + '/media/html/admin_apache.html',
            'admin_aws': MEDIA_ROOT + '/media/html/admin_aws.html',
            'admin_ga': MEDIA_ROOT + '/media/html/admin_ga.html',
            'admin_git': MEDIA_ROOT + '/media/html/admin_git.html',
            'admin_backup': MEDIA_ROOT + '/media/html/admin_backup.html',
            'admin_dir': MEDIA_ROOT + '/media/html/admin_dir.html',
            'admin_doc': MEDIA_ROOT + '/media/html/admin_doc.html',
            'admin_export': MEDIA_ROOT + '/media/html/admin_export.html',

            '400': MEDIA_ROOT + '/media/html/error_400.html',
            '401': MEDIA_ROOT + '/media/html/error_401.html',
            '403': MEDIA_ROOT + '/media/html/error_403.html',
            '404': MEDIA_ROOT + '/media/html/error_404.html',
            '500': MEDIA_ROOT + '/media/html/error_500.html',
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

            'TMPDIR': MEDIA_ROOT + '/temp/',

        }

