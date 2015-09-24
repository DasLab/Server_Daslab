import os

# from config.t47_dev import T47_DEV as DEBUG
from src.settings import env

from django.contrib.auth import authenticate, login, logout

MEDIA_ROOT = os.path.dirname(os.path.dirname(__file__))

class USER_GROUP:
    def __init__(self):
        f = open('%s/config/group.conf' % MEDIA_ROOT, 'r')
        lines = f.readlines()
        f.close()

        self.ADMIN = lines[0].replace('daslab_admin: ', '').split(' ')
        self.GROUP = lines[1].replace('daslab_group: ', '').split(' ')
        self.ALUMNI = lines[2].replace('daslab_alumni: ', '').split(' ')
        self.ROTON = lines[3].replace('daslab_roton: ', '').split(' ')
        self.OTHER = lines[4].replace('daslab_other: ', '').split(' ')


class AutomaticAdminLoginMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, 'user') or not request.user.is_authenticated():
            try:
                sunet_id = request.META['WEBAUTH_USER']
                is_admin = (sunet_id in USER_GROUP().ADMIN)
            except:
                is_admin = False

            print "middleware:", is_admin
            if is_admin:
                user = authenticate(username=env('APACHE_USER'), password=env('APACHE_PASSWORD'))
                request.user = user
                login(request, user)

