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
        self.msg_handles = []

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
            who_id = ''
        return who_id

    def compose_msg(self, task_tuple, task_name, interval):
        who_main = self.find_slack_id(task_tuple[0])
        who_bkup = self.find_slack_id(task_tuple[1])
        if who_main:
            msg = '*LAB DUTY*: Just a reminder for the _%s_ check of `%s`. If you are unable to do so, please inform the ' % (interval, task_name)
            if who_bkup:
                msg += 'backup person for this task: _%s_ <@%s>.' % (task_tuple[1], who_bkup)
            else:
                msg += 'site admin <@%s> since there is *NO* backup person for this task.' % SLACK['ADMIN_NAME']
            self.msg_handles.append( ('@' + who_main, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":msg }]) )


    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))
         
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

            if flag == 'weekly':
                breakfast = ppls['weekly']['breakfast']
                who_main = self.find_slack_id(breakfast[0])
                who_bkup = self.find_slack_id(breakfast[1])
                if who_main:
                    if who_bkup:
                        self.msg_handles.append( ('@' + who_main, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":'*LAB DUTY*: Just a reminder that you are up for bringing `Breakfast` for _tomorrow_. If you are unable to do so, please inform the backup person for this task: _%s_ <@%s>.' % (breakfast[1], who_bkup)}]) )
                    else:
                        self.msg_handles.append( ('@' + who_main, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":'*LAB DUTY*: Just a reminder that you are up for bringing `Breakfast` for _tomorrow_. If you are unable to do so, please inform the site admin <@%s> since there is no backup person for this task.' % SLACK['ADMIN_NAME']}]) )                        

                if result['this'][1] == 'ES':
                    microphone = ppls['monthly']['microphone']
                    who_main = self.find_slack_id(microphone[0])
                    who_bkup = self.find_slack_id(microphone[1])
                    if who_main:
                        if who_bkup:
                        self.msg_handles.append( ('@' + who_main, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":'*LAB DUTY*: Just a reminder that you are up for `Microphone Setup` for _Eterna Open Group Meeting_. Please arrive *30 min* early. If you are unable to do so, please inform the backup person for this task: _%s_ <@%s>.' % (microphone[1], who_bkup)}]) )
                    else:
                        self.msg_handles.append( ('@' + who_main, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":'*LAB DUTY*: Just a reminder that you are up for `Microphone Setup` for _Eterna Open Group Meeting_. Please arrive *30 min* early. If you are unable to do so, please inform the site admin <@%s> since there is no backup person for this task.' % SLACK['ADMIN_NAME']}]) )                        

            elif flag == 'monthly':
                compose_msg(self, ppls[flag]['amazon'], 'Amazon Web Services', flag)
                compose_msg(self, ppls[flag]['website'], 'Website', flag)
                compose_msg(self, ppls[flag]['birthday'], 'Birthday Celebrations', flag)
                compose_msg(self, ppls[flag]['group meeting'], 'Meeting Scheduling', flag)
            elif flag == 'quarterly':
                compose_msg(self, ppls[flag]['lab trips'], 'Lab Outing/Trips', flag)
                compose_msg(self, ppls[flag]['github'], 'Mailing, Slack, GitHub', flag)

        except subprocess.CalledProcessError:
            err = traceback.format_exc()
            ts = '%s\t\t%s\n' % (time.ctime(), ' '.join(sys.argv))
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_duty.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
            if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *%s* @ _%s_\n>```%s```\n' % (' '.join(sys.argv), time.ctime(), err)}])
            self.stdout.write("Finished with \033[41mERROR\033[0m!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(1)

        else:
            for h in self.msg_handles:
                send_notify_slack(h[0], h[1], h[2])
                if '@' in h[0]:
                    self.stdout.write('\033[92mSUCCESS\033[0m: PM\'ed duty reminder to \033[94m%s\033[0m in Slack.' % h[0])
    
        if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'SUCCESS', "mrkdwn_in": ["text"], "color":"good", "text":'*SUCCESS*: Scheduled %s *duty reminder* finished @ _%s_\n' % (flag, time.ctime())}])
        self.stdout.write("Finished with \033[92mSUCCESS\033[0m!")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
        sys.exit(0)
