# from src.settings import env

from django.contrib.auth import authenticate, login, logout


class USER_GROUP(object):
    def __init__(self, MEDIA_ROOT):
        lines = open('%s/config/group.conf' % MEDIA_ROOT, 'r').readlines()

        self.ADMIN = [ x.strip() for x in lines[0].replace('daslab_admin: ', '').split(' ')]
        self.GROUP = [ x.strip() for x in lines[1].replace('daslab_group: ', '').split(' ')]
        self.ALUMNI = [ x.strip() for x in lines[2].replace('daslab_alumni: ', '').split(' ')]
        self.OTHER = [ x.strip() for x in lines[3].replace('daslab_other: ', '').split(' ')]
        self.ROTON = [ x.strip() for x in lines[4].replace('daslab_roton: ', '').split(' ')]


class AutomaticAdminLoginMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, 'user') or not request.user.is_authenticated():
            try:
                sunet_id = request.META['WEBAUTH_USER']
                is_admin = (sunet_id in USER_GROUP().ADMIN)
            except:
                is_admin = False

            # print "middleware:", is_admin
            if is_admin:
                user = authenticate(username=env('APACHE_USER'), password=env('APACHE_PASSWORD'))
                request.user = user
                login(request, user)


class ExceptionUserInfoMiddleware(object):
    def process_exception(self, request, exception):
        try:
            if request.user.is_authenticated():
                request.META['USERNAME'] = str(request.user.username)
                request.META['USER_EMAIL'] = str(request.user.email)
        except:
            pass
