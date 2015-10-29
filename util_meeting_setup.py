from datetime import datetime, timedelta
import os
import pickle
import requests
import smtplib
import subprocess
import sys
import time
import traceback

from django.core.wsgi import get_wsgi_application
sys.path.append(os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings") 
application = get_wsgi_application()

from slacker import Slacker
from src.settings import *
from src.models import FlashSlide
from src.console import send_notify_emails, send_notify_slack


t0 = time.time()
print time.ctime()

try:
    result = pickle.load(open('%s/cache/schedule.pickle' % MEDIA_ROOT, 'rb'))
    sh = Slacker(SLACK["ACCESS_TOKEN"])
    users = sh.users.list().body['members']
    msg_handles = []

    year = (datetime.utcnow() + timedelta(days=1)).date().year
    date = datetime.strptime("%s %s" % (result['this'][0], year), '%b %d %Y')
    title = 'Flash Slides: %s' % datetime.strftime(date, '%b %d %Y')
    if result['this'][1] != 'N/A':
        access_token = requests.post('https://www.googleapis.com/oauth2/v3/token?refresh_token=%s&client_id=%s&client_secret=%s&grant_type=refresh_token' % (DRIVE['REFRESH_TOKEN'], DRIVE['CLIENT_ID'], DRIVE['CLIENT_SECRET'])).json()['access_token']
        temp = requests.post('https://www.googleapis.com/drive/v2/files/%s/copy?access_token=%s' % (DRIVE['PRESENTATION_ID'], access_token), json={"title":"%s" % title})
        ppt_id = temp.json()['id']
        temp = requests.post('https://www.googleapis.com/drive/v2/files/%s/permissions?sendNotificationEmails=false&access_token=%s' % (ppt_id, access_token), json={"role":"writer", "type":"group", "value":"das-lab@googlegroups.com"})
        print '\033[92mSUCCESS\033[0m: Google Presentation (\033[94m%s\033[0m) created and shared.' % ppt_id

        msg_handles.append( ('#general', '', [{"fallback":'%s' % title, "mrkdwn_in": ["text"], "color":"warning", "title":'%s' % title, "text":'*<https://docs.google.com/presentation/d/%s/edit#slide=id.p>*\n_This link could also be found on the Das Lab <https://daslab.stanford.edu/group/flash_slide/|website>_' % ppt_id, "thumb_url":'https://daslab.stanford.edu/site_media/images/group/logo_drive.png'}]))
        flash_slides = FlashSlide(date=date, link='https://docs.google.com/presentation/d/%s/edit#slide=id.p' % ppt_id)
        flash_slides.save()
        print '\033[92mSUCCESS\033[0m: Google Presentation (\033[94m%s\033[0m) saved in MySQL.' % ppt_id
    else:
        print '\033[92mSUCCESS\033[0m: Google Presentation skipped (N/A for this week: \033[94m%s\033[0m).' % datetime.strftime(date, '%b %d %Y')

    clock = result['tp'][result['tp'].find('@')+1:result['tp'].rfind('@')].strip()
    clock = clock[:clock.find('-')].strip()
    place = result['tp'][result['tp'].rfind('@')+1:].strip()[:-1]
    types = {'ES':'EteRNA Special', 'GM':'Group Meeting', 'JC':'Journal Club'}
    if result['this'][1] == 'N/A':
        msg_this = 'This is a reminder that there will be `NO Meeting` this week.'
    else:
        type_this = types[result['this'][1]]
        msg_this = 'This is a reminder that group meeting will be `%s` for this week.\n# Date: _%s_\n# Time: *%s*\n# Place: %s\n# Presenter: _*%s*_\n# Type: `%s`\n# Flash Slides: <https://docs.google.com/presentation/d/%s/edit#slide=id.p>' % (type_this, datetime.strftime(date, '%b %d %Y (%a)'), clock, place, result['this'][2], type_this, ppt_id)

        flag = result['this'][3].lower().replace(' ', '')
        if flag == 'endofrotationtalk':
            name = result['this'][2]
            if '/' in name or '&' in name:
                names = name.replace('/', '*|*').replace('&', '*|*').replace(' ', '').split('*|*')
            else:
                names = [name]
            for name in names:
                sunet_id = 'none'
                for resp in users:
                    if resp.has_key('is_bot') and resp['is_bot']: continue
                    if resp['profile']['real_name'][:len(name)].lower() == name.lower():
                        if sunet_id != 'none': 
                            sunet_id = 'ambiguous'
                            break
                        email = resp['profile']['email']
                        sunet_id = email[:email.find('@')]
                        who_id = resp['name']

                if sunet_id in GROUP.ROTON:
                    msg_who = 'Just a reminder: Please send your presentation to %s (site admin) for `archiving` *after* your presentation _tomorrow_.' % SLACK['ADMIN_NAME']
                    msg_handles.append( ('@' + who_id, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"good", "text":msg_who}]))
                else:
                    if sunet_id == 'none':
                        print '\033[41mERROR\033[0m: rotation student (\033[94m%s\033[0m) not found.' % name
                    elif sunet_id == 'ambiguous':
                        print '\033[41mERROR\033[0m: rotation student (\033[94m%s\033[0m) is ambiguate (more than 1 match).' % name
                    else:
                        print '\033[41mERROR\033[0m: rotation student (\033[94m%s\033[0m) not available in database.' % name
            msg_handles.append( (SLACK['ADMIN_NAME'], '', [{"fallback":'REMINDER', "mrkdwn_in": ["text"], "color":"warning", "text":'*REMINDER*: Add *RotationStudent* entry for _%s_.' % datetime.strftime(date, '%b %d %Y (%a)')}]) )

        if result['this'][1] == 'JC':
            msg_handles.append( (SLACK['ADMIN_NAME'], '', [{"fallback":'REMINDER', "mrkdwn_in": ["text"], "color":"warning", "text":'*REMINDER*: Add *JournalClub* entry for _%s_.' % datetime.strftime(date, '%b %d %Y (%a)')}]) )
        elif result['this'][1] == 'ES':
            msg_handles.append( (SLACK['ADMIN_NAME'], '', [{"fallback":'REMINDER', "mrkdwn_in": ["text"], "color":"warning", "text":'*REMINDER*: Add *EternaYoutube* entry for _%s_.' % datetime.strftime(date, '%b %d %Y (%a)')}]) )


    if result['next'][1] == 'N/A':
        msg_next = 'For next week, there will be `NO Meeting`.'
    else:
        type_next = types[result['next'][1]]
        year = (datetime.utcnow() + timedelta(days=8)).date().year
        date = datetime.strptime("%s %s" % (result['next'][0], year), '%b %d %Y')
        msg_next = 'For next week:\n# Date: _%s_\n# Time: *%s*\n# Place: %s\n# Presenter: _*%s*_\n# Type: `%s`' % (datetime.strftime(date, '%b %d %Y (%a)'), clock, place, result['next'][2], type_next)

        msg_who = 'Just a reminder that you are up for `%s` *next* _%s_ (*%s*).\n' % (type_next, datetime.strftime(date, '%A'), datetime.strftime(date, '%b %d'))
        if result['next'][1] == 'JC':
            date = (datetime.utcnow() + timedelta(days=5)).date()
            msg_who += ' Please post your paper of choice to the group `#general` channel by *next* _%s_ (*%s*).\n' % (datetime.strftime(date, '%A'), datetime.strftime(date, '%b %d'))
        elif result['next'][1] == 'ES':
            date = (datetime.utcnow() + timedelta(days=6)).date()
            msg_who += ' Please post a brief description of the topic to the group `#general` channel by *next* _%s_ (*%s*) to allow time for releasing news on both DasLab Website and EteRNA broadcast.\n' % (datetime.strftime(date, '%A'), datetime.strftime(date, '%b %d'))

        name = result['next'][2]
        if '/' in name or '&' in name:
            names = name.replace('/', '*|*').replace('&', '*|*').replace(' ', '').split('*|*')
        else:
            names = [name]
        if name:
            for name in names:
                sunet_id = 'none'
                for resp in users:
                    if resp.has_key('is_bot') and resp['is_bot']: continue
                    if resp['profile']['real_name'][:len(name)].lower() == name.lower():
                        if sunet_id != 'none': 
                            sunet_id = 'ambiguous'
                            break
                        email = resp['profile']['email']
                        sunet_id = email[:email.find('@')]
                        who_id = resp['name']

                if sunet_id in GROUP.ADMIN or sunet_id in GROUP.GROUP or sunet_id in GROUP.ALUMNI or sunet_id in GROUP.ROTON or sunet_id in GROUP.OTHER:
                    msg_handles.append( ('@' + who_id, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"good", "text":msg_who}]))
                else:
                    if sunet_id == 'none':
                        print '\033[41mERROR\033[0m: member (\033[94m%s\033[0m) not found.' % name
                    elif sunet_id == 'ambiguous':
                        print '\033[41mERROR\033[0m: member (\033[94m%s\033[0m) is ambiguate (more than 1 match).' % name
                    else:
                        print '\033[41mERROR\033[0m: member (\033[94m%s\033[0m) not available in database.' % name

    post = '''Hi all,\n\n%s\n\n%s\n\nThe full schedule is on the Das Lab <https://daslab.stanford.edu/group/schedule/|website>. For questions regarding the schedule, please contact _%s_ (site admin). Thanks for your attention.''' % (msg_this, msg_next, SLACK['ADMIN_NAME'])
    msg_handles.append( ('#general', '*Group Meeting Reminder*', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"439fe0", "text":post, "thumb_url":'https://daslab.stanford.edu/site_media/images/group/logo_bot.jpg'}]) )


except:
    err = traceback.format_exc()
    ts = '%s\t\t%s\n' % (time.ctime(), sys.argv[0])
    open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
    open('%s/cache/log_cron_meeting.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))

    if result['this'][1] != 'N/A':
        year = (datetime.utcnow() + timedelta(days=1)).date().year
        date = datetime.strptime("%s %s" % (result['this'][0], year), '%b %d %Y')
        FlashSlide.objects.get(date=date).delete()
        requests.delete('https://www.googleapis.com/drive/v2/files/%s/?access_token=%s' % (ppt_id, access_token))
        print '\033[92mSUCCESS\033[0m: Google Presentation (\033[94m%s\033[0m) deleted.' % ppt_id
        print '\033[92mSUCCESS\033[0m: Google Presentation (\033[94m%s\033[0m) removed in MySQL.' % ppt_id

    if IS_SLACK:
        send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *%s* @ _%s_\n>```%s```\n' % (sys.argv[0], time.ctime(), err)}])
        send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"warning", "text":'FlashSlide table in MySQL database, presentation in Google Drive, and posted messages in Slack are rolled back.\nFlash Slide has *`NOT`* been setup yet for this week! Please investigate and fix the setup immediately.'}])
    else:
        send_notify_emails('[Django] {daslab.stanford.edu} ERROR: Weekly Meeting Setup', 'This is an automatic email notification for the failure of scheduled weekly flash slides setup. The following error occurred:\n\n%s\n\n%s\n\nFlashSlide table in MySQL database, presentation in Google Drive, and posted messages in Slack are rolled back.\n\n** Flash Slide has NOT been setup yet for this week! Please investigate and fix the setup immediately.\n\nDasLab Website Admin' % (ts, err))

    print "Finished with \033[41mERROR\033[0m!"
    print "Time elapsed: %.1f s." % (time.time() - t0)
    sys.exit(1)

else:
    for h in msg_handles:
        send_notify_slack(h[0], h[1], h[2])
        if '@' in h[0]:
            print '\033[92mSUCCESS\033[0m: PM\'ed reminder to \033[94m%s\033[0m in Slack.' % h[0]
    print '\033[92mSUCCESS\033[0m: Google Presentation posted in Slack.'
    print '\033[92mSUCCESS\033[0m: Meeting Reminder posted in Slack.'

if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'SUCCESS', "mrkdwn_in": ["text"], "color":"good", "text":'*SUCCESS*: Scheduled weekly *flash slides setup* finished @ _%s_\n' % time.ctime()}])
print "Finished with \033[92mSUCCESS\033[0m!"
print "Time elapsed: %.1f s." % (time.time() - t0)
sys.exit(0)

