# from src.settings import env

from django.contrib.auth import authenticate, login
# import os
# import traceback

from src.env import MEDIA_ROOT, env, Singleton
# MEDIA_ROOT = os.path.dirname(os.path.dirname(__file__))


class USER_GROUP(Singleton):
    def __init__(self):
        lines = open('%s/config/group.conf' % MEDIA_ROOT, 'r').readlines()

        self.ADMIN = [x.strip() for x in lines[0].replace('daslab_admin: ', '').split(' ')]
        self.GROUP = [x.strip() for x in lines[1].replace('daslab_group: ', '').split(' ')]
        self.ALUMNI = [x.strip() for x in lines[2].replace('daslab_alumni: ', '').split(' ')]
        self.OTHER = [x.strip() for x in lines[3].replace('daslab_other: ', '').split(' ')]
        self.ROTON = [x.strip() for x in lines[4].replace('daslab_roton: ', '').split(' ')]

    def find_type(self, sunet_id):
        if sunet_id in self.ADMIN:
            return 'admin'
        elif sunet_id in self.GROUP:
            return 'group'
        elif sunet_id in self.ALUMNI:
            return 'alumni'
        elif sunet_id in self.ROTON:
            return 'roton'
        elif sunet_id in self.OTHER:
            return 'other'
        else:
            return 'unknown'


class AutomaticAdminLoginMiddleware(object):
    def process_request(self, request):
        if (not hasattr(request, 'user') or
            not request.user.is_authenticated()):
            try:
                sunet_id = request.META['WEBAUTH_USER']
                is_admin = USER_GROUP().find_type(sunet_id) == 'admin'
            except Exception:
                is_admin = False
                # print traceback.format_exc()

            if is_admin:
                user = authenticate(
                    username=env('DJANGO_USER'),
                    password=env('DJANGO_PASSWORD')
                )
                request.user = user
                login(request, user)


class ExceptionUserInfoMiddleware(object):
    def process_exception(self, request, exception):
        try:
            if request.user.is_authenticated():
                request.META['USERNAME'] = str(request.user.username)
                request.META['USER_EMAIL'] = str(request.user.email)
        except Exception:
            pass


GROUP = USER_GROUP()
MANAGERS = ADMINS = (
    (env('ADMIN_NAME'), env('ADMIN_EMAIL')),
)
if bool(int(env('EXTRA_NOTIFY'))):
    ADMINS = (
        ADMINS[0],
        (env('EXTRA_NAME'), env('EXTRA_EMAIL'))
    )
EMAIL_NOTIFY = env('ADMIN_EMAIL')
(EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_USE_TLS, EMAIL_PORT, EMAIL_HOST) = [
    v for k, v in env.email_url().items()
    if k in ['EMAIL_HOST_PASSWORD', 'EMAIL_HOST_USER', 'EMAIL_USE_TLS', 'EMAIL_PORT', 'EMAIL_HOST']
]
EMAIL_SUBJECT_PREFIX = '{%s}' % env('SERVER_NAME')
