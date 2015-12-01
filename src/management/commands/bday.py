import datetime
import subprocess
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from slacker import Slacker

from src.settings import *
from src.models import Member
from src.console import send_notify_slack


class Command(BaseCommand):
    help = 'Send out individual birthday wishes in Slack.'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.sh = Slacker(SLACK["ACCESS_TOKEN"])
        self.users = self.sh.users.list().body['members']


    def find_slack_id(self, name):
        sunet_id = 'none'
        who_id = ''
        for resp in self.users:
            if resp.has_key('is_bot') and resp['is_bot']: continue
            if resp['profile']['real_name'][:len(name)].lower() == name.lower():
                if sunet_id != 'none': 
                    sunet_id = 'ambiguous'
                    break
                email = resp['profile']['email']
                sunet_id = email[:email.find('@')]
                who_id = resp['name']

        if sunet_id == 'none':
            self.stdout.write('\033[41mERROR\033[0m: member (\033[94m%s\033[0m) not found.' % name)
        elif sunet_id == 'ambiguous':
            self.stdout.write('\033[41mERROR\033[0m: member (\033[94m%s\033[0m) is ambiguate (more than 1 match).' % name)
            who_id = ''
        return who_id


    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))
         
        try:
            msg_handles, ids, names = [], [], []
            today_str = datetime.date.today().strftime('%m/%d')
            member = Member.objects.filter(alumni=0, bday=today_str)
            for ppl in member:
                who = self.find_slack_id(ppl.first_name)
                if who:
                    send_to = '@' + who
                    if DEBUG: send_to = SLACK['ADMIN_NAME']
                    msg_handles.append( (send_to, '', [{"fallback":'BDay', "mrkdwn_in": ["text"], "color":"ff912e", "text":'*Happy Birthday*, _%s_!' % ppl.first_name}]) )
                    ids.append(who)
                    names.append(ppl.first_name)
            if ids and (not DEBUG):
                msg_handles.append( ('#general', '', [{"fallback":'BDay', "mrkdwn_in": ["text"], "color":"ff912e", "text":'*Happy Birthday* to _%s_! %s' % (' '.join(names), ' '.join( ['<@' + id + '>' for id in ids] ))}]) )

        except:
            err = traceback.format_exc()
            ts = '%s\t\t%s\n' % (time.ctime(), ' '.join(sys.argv))
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_bday.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
            if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *%s* @ _%s_\n>```%s```\n' % (' '.join(sys.argv), time.ctime(), err)}])
            self.stdout.write("Finished with \033[41mERROR\033[0m!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(1)

        else:
            for h in msg_handles:
                send_notify_slack(h[0], h[1], h[2])
                if '@' in h[0]:
                    self.stdout.write('\033[92mSUCCESS\033[0m: PM\'ed birthday wish to \033[94m%s\033[0m in Slack.' % h[0])
        if msg_handles and IS_SLACK: 
            send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'SUCCESS', "mrkdwn_in": ["text"], "color":"good", "text":'*SUCCESS*: Scheduled *birthday wish* sent to `%s` @ _%s_\n' % (' '.join(ids), time.ctime())}])
            self.stdout.write("Finished with \033[92mSUCCESS\033[0m!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
