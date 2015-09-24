import os

from config.t47_dev import T47_DEV as DEBUG

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
