from datetime import datetime, timedelta
import os
import pickle
import requests
import subprocess
import sys
import time
import traceback

sys.path.append(os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings") 

from slacker import Slacker
from src.settings import *

t0 = time.time()
print time.ctime()
t = time.time()

try:
    f = open('%s/cache/schedule.pickle' % MEDIA_ROOT, 'rb')
    result = pickle.load(f)
    f.close()
    title = 'Flash Slides: %s' % result['this'][0]
    year = (datetime.utcnow() + timedelta(days=1)).date().year
    if result['this'][1] != 'N/A':
        access_token = requests.post('https://www.googleapis.com/oauth2/v3/token?refresh_token=%s&client_id=%s&client_secret=%s&grant_type=refresh_token' % (DRIVE['REFRESH_TOKEN'], DRIVE['CLIENT_ID'], DRIVE['CLIENT_SECRET'])).json()['access_token']
        temp = requests.post('https://www.googleapis.com/drive/v2/files/%s/copy?access_token=%s' % (DRIVE['PRESENTATION_ID'], access_token), json={"title":"Flash Slides: %s %s" % (title, year)})
        id = temp.json()['id']
        temp = requests.post('https://www.googleapis.com/drive/v2/files/%s/permissions?access_token=%s' % (id, access_token), json={"role":"writer", "type":"group", "value":"das-lab@googlegroups.com"})

    clock = result['tp'][result['tp'].find('@')+1:result['tp'].rfind('@')].strip()
    clock = clock[:clock.find('-')].strip()
    place = result['tp'][result['tp'].rfind('@')+1:].strip()[:-1]
    types = {'ES':'EteRNA Special', 'GM':'Group Meeting', 'JC':'Journal Club'}
    if result['this'][1] == 'N/A':
        msg_this = 'This is a reminder that there will be `NO Meeting` this week.'
    else:
        type_this = types[result['this'][1]]
        msg_this = 'This is a reminder that group meeting will be `%s` for this week.\n# Date: _%s %s_\n# Time: *%s*\n# Place: %s\n# Presenter: _*%s*_\nType: `%s`\n# Flash Slides: <https://docs.google.com/presentation/d/%s/edit#slide=id.p>' % (type_this, result['this'][0], year, clock, place, result['this'][2], type_this, id)
    if result['next'][1] == 'N/A':
        msg_next = 'For next week, there will be `NO Meeting`.'
    else:
        type_next = types[result['next'][1]]
        year = (datetime.utcnow() + timedelta(days=8)).date().year
        msg_next = 'For next week:\n# Date: _%s %s_\n# Time: *%s*\n# Place: %s\n# Presenter: _*%s*_\n# Type: `%s`' % (result['next'][0], year, clock, place, result['next'][2], type_next)
    post = '''Hi all,\n%s\n\n%s\n\nThe full schedule is on the Das Lab <https://daslab.stanford.edu/group/schedule/|website>. Thanks for your attention.''' % (msg_this, msg_next)

    sh = Slacker(SLACK["ACCESS_TOKEN"])
    if result['this'][1] != 'N/A':
        sh.chat.post_message('#general', '>*<https://docs.google.com/presentation/d/%s/edit#slide=id.p|%s>*' % (id, title), as_user=False, parse='none', username='DasLab Bot')
    sh.chat.post_message('#general', post, as_user=False, parse='none', username='DasLab Bot')

except:
    print traceback.format_exc()
    print "Finished with \033[41mERROR\033[0m!"
    print "Time elapsed: %.1f s." % (time.time() - t0)
    sys.exit(1)

print "Finished with \033[92mSUCCESS\033[0m!"
print "Time elapsed: %.1f s." % (time.time() - t0)
sys.exit(0)

