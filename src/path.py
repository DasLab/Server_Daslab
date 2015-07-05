import os

MEDIA_ROOT = os.path.dirname(os.path.dirname(__file__))

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
            'profile': MEDIA_ROOT + '/media/html/_profile.html',

            'lab_meetings': MEDIA_ROOT + '/media/html/lab_meetings.html',
            'lab_calendar': MEDIA_ROOT + '/media/html/lab_calendar.html',
            'lab_resources': MEDIA_ROOT + '/media/html/lab_resources.html',
            'lab_misc': MEDIA_ROOT + '/media/html/lab_misc.html',

            'admin_apache': MEDIA_ROOT + '/media/admin/_apache.html',
            'admin_backup': MEDIA_ROOT + '/media/admin/_backup.html',
            'admin_dir': MEDIA_ROOT + '/media/admin/_dir.html',
            'admin_doc': MEDIA_ROOT + '/media/admin/_doc.html',

            '403': MEDIA_ROOT + '/media/html/_403.html',
            '404': MEDIA_ROOT + '/media/html/_404.html',
            '500': MEDIA_ROOT + '/media/html/_500.html',
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

