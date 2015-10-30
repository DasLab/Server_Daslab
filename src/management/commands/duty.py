import pickle
import subprocess
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.console import send_notify_slack


class Command(BaseCommand):
    help = 'Send out individual Responsibility Reminder notifications in Slack.'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.sh = Slacker(SLACK["ACCESS_TOKEN"])
        self.users = self.sh.users.list().body['members']

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('interval', nargs='+', type=str, help='Interval, choose from (week, month, quarter).')


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
        return who_id


    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write(time.ctime())
         
        if options['interval']:
            flag = options['interval'][0] + 'ly'
        else:
            self.stdout.write('\033[41mERROR\033[0m: \033[94minterval\033[0m not found.')
            self.stdout.write("Finished with \033[41mERROR\033[0m!")
            sys.exit(1)

        try:
            gdrive_dir = 'cd %s/cache' % MEDIA_ROOT
            gdrive_mv = 'mv Das\ Lab\ Responsibilities.csv duty.csv'
            subprocess.check_call("%s && drive download --format csv --force -i %s && %s" % (gdrive_dir, DRIVE["DUTY_SPREADSHEET_ID"], gdrive_mv), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            lines = open('%s/cache/duty.csv' % MEDIA_ROOT, 'r').readlines()

            ppls = {'weekly':{}, 'monthly':{}, 'quarterly':{}}
            jobs = ['birthday', 'breakfast', 'microphone', 'group meeting', 'lab trips', 'amazon', 'website', 'github']
            for row in lines[1:-6]:
                row = row.split(',')
                for job in jobs:
                    if job in row[0].lower():
                        ppls[row[1].lower()][job] = (row[2], row[3])

            result = pickle.load(open('%s/cache/schedule.pickle' % MEDIA_ROOT, 'rb'))
            msg_handles = []

            if flag == 'weekly':
                breakfast = ppls['weekly']['breakfast']
                who_main = self.find_slack_id(breakfast[0])
                who_bkup = self.find_slack_id(breakfast[1])
                msg_handles.append( ('@' + who_main, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":'*LAB DUTY*: Just a reminder that you are up for bringing `Breakfast` for _tomorrow_. If you are unable to do so, please inform the backup person for this task: _%s_ <@%s>.' % (breakfast[1], who_bkup)}]) )

                if result['this'][1] == 'ES':
                    microphone = ppls['monthly']['microphone']
                    who_main = self.find_slack_id(microphone[0])
                    who_bkup = self.find_slack_id(microphone[1])
                    msg_handles.append( ('@' + who_main, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":'*LAB DUTY*: Just a reminder that you are up for `Microphone Setup` for _Eterna Open Group Meeting_. Please arrive *30 min* early. If you are unable to do so, please inform the backup person for this task: _%s_ <@%s>.' % (microphone[1], who_bkup)}]) )

            elif flag == 'monthly':
                amazon = ppls['monthly']['amazon']
                who_main = self.find_slack_id(amazon[0])
                who_bkup = self.find_slack_id(amazon[1])
                msg_handles.append( ('@' + who_main, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":'*LAB DUTY*: Just a reminder for the _monthly_ check of `Amazon Web Services`. If you are unable to do so, please inform the backup person for this task: _%s_ <@%s>.' % (amazon[1], who_bkup)}]) )

                website = ppls['monthly']['website']
                who_main = self.find_slack_id(website[0])
                who_bkup = self.find_slack_id(website[1])
                msg_handles.append( ('@' + who_main, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":'*LAB DUTY*: Just a reminder for the _monthly_ check of `Website`. If you are unable to do so, please inform the backup person for this task: _%s_ <@%s>.' % (website[1], who_bkup)}]) )

                birthday = ppls['monthly']['birthday']
                who_main = self.find_slack_id(birthday[0])
                who_bkup = self.find_slack_id(birthday[1])
                msg_handles.append( ('@' + who_main, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":'*LAB DUTY*: Just a reminder for the _monthly_ check of `Birthday Celebrations`. If you are unable to do so, please inform the backup person for this task: _%s_ <@%s>.' % (birthday[1], who_bkup)}]) )

                meeting = ppls['monthly']['group meeting']
                who_main = self.find_slack_id(meeting[0])
                who_bkup = self.find_slack_id(meeting[1])
                msg_handles.append( ('@' + who_main, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":'*LAB DUTY*: Just a reminder for the _monthly_ check of `Meeting Schedule`. If you are unable to do so, please inform the backup person for this task: _%s_ <@%s>.' % (meeting[1], who_bkup)}]) )

            elif flag == 'quarterly':
                outing = ppls['quarterly']['lab trips']
                who_main = self.find_slack_id(outing[0])
                who_bkup = self.find_slack_id(outing[1])
                msg_handles.append( ('@' + who_main, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":'*LAB DUTY*: Just a reminder for the _quarterly_ `Lab Trips`. If you are unable to do so, please inform the backup person for this task: _%s_ <@%s>.' % (outing[1], who_bkup)}]) )

                github = ppls['quarterly']['github']
                who_main = self.find_slack_id(github[0])
                who_bkup = self.find_slack_id(github[1])
                msg_handles.append( ('@' + who_main, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":'*LAB DUTY*: Just a reminder for the _quarterly_ check of `Mailing, Slack, GitHub`. If you are unable to do so, please inform the backup person for this task: _%s_ <@%s>.' % (github[1], who_bkup)}]) )


        except subprocess.CalledProcessError:
            err = traceback.format_exc()
            ts = '%s\t\t%s %s %s\n' % (time.ctime(), sys.argv[0], sys.argv[1], flag)
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_duty.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
            if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *%s %s %s* @ _%s_\n>```%s```\n' % (sys.argv[0], sys.argv[1], flag, time.ctime(), err)}])
            self.stdout.write("Finished with \033[41mERROR\033[0m!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(1)

        else:
            for h in msg_handles:
                send_notify_slack(h[0], h[1], h[2])
                if '@' in h[0]:
                    self.stdout.write('\033[92mSUCCESS\033[0m: PM\'ed duty reminder to \033[94m%s\033[0m in Slack.' % h[0])
    
        if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'SUCCESS', "mrkdwn_in": ["text"], "color":"good", "text":'*SUCCESS*: Scheduled %s *duty reminder* finished @ _%s_\n' % (flag, time.ctime())}])
        self.stdout.write("Finished with \033[92mSUCCESS\033[0m!")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
        sys.exit(0)
