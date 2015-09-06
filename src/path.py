import os

MEDIA_ROOT = os.path.dirname(os.path.dirname(__file__))

class SYS_PATH:
    def __init__(self):
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
            'profile': MEDIA_ROOT + '/media/html/group_profile.html',

            'lab_meetings': MEDIA_ROOT + '/media/html/group_meetings.html',
            'lab_calendar': MEDIA_ROOT + '/media/html/group_calendar.html',
            'lab_documents': MEDIA_ROOT + '/media/html/group_documents.html',
            'lab_services': MEDIA_ROOT + '/media/html/group_services.html',
            'lab_servers': MEDIA_ROOT + '/media/html/group_servers.html',
            'lab_misc': MEDIA_ROOT + '/media/html/group_misc.html',

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

