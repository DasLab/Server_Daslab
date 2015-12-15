from datetime import datetime, timedelta
import pickle
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

    def compose_msg(self, task_tuple, task_name, interval, alt_text):
        who_main = self.find_slack_id(task_tuple[0])
        who_bkup = self.find_slack_id(task_tuple[1])
        if who_main:
            msg = '*LAB DUTY*: Just a reminder for the _%s_ task of `%s`%s. If you are unable to do so, please inform the ' % (interval, task_name, alt_text)
            if who_bkup:
                msg += 'backup person for this task: _%s_ <@%s>.' % (task_tuple[1], who_bkup)
            else:
                msg += 'site admin <@%s> since there is *NO* backup person for this task.' % SLACK['ADMIN_NAME']
            send_to = '@' + who_main
            if DEBUG: send_to = SLACK['ADMIN_NAME']
            self.msg_handles.append( (send_to, '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"c28fdd", "text":msg }]) )
        else:
            self.msg_handles.append( (SLACK['ADMIN_NAME'], '', [{"fallback":'Reminder', "mrkdwn_in": ["text"], "color":"ff912e", "text": '*WARNING*: No one is primarily assigned for the duty of _%s_ check of `%s`. *NO* reminder sent.' % (intern, task_name) }]) )



    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))
         
        if options['interval']:
            if options['interval'][0][-2:] == 'ly':
                flag = options['interval'][0]
            else:
                flag = options['interval'][0] + 'ly'
        else:
            self.stdout.write('\033[41mERROR\033[0m: \033[94minterval\033[0m not found.')
            self.stdout.write("Finished with \033[41mERROR\033[0m!")
            sys.exit(1)

        if flag in ['monthly', 'quarterly']:
            if datetime.utcnow().date().day > 7:
                return

        try:
            gdrive_dir = 'cd %s/cache' % MEDIA_ROOT
            gdrive_mv = 'mv Das\ Lab\ Responsibilities.csv duty.csv'
            subprocess.check_call("%s && drive download --format csv --force -i %s && %s" % (gdrive_dir, DRIVE["DUTY_SPREADSHEET_ID"], gdrive_mv), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            lines = open('%s/cache/duty.csv' % MEDIA_ROOT, 'r').readlines()

            ppls = {'weekly':{}, 'monthly':{}, 'quarterly':{}}
            jobs = ['birthday', 'breakfast', 'eterna', 'group meeting', 'lab trips', 'amazon', 'website', 'github']
            for row in lines[1:-6]:
                row = row.split(',')
                for job in jobs:
                    if job in row[0].lower():
                        ppls[row[1].lower()][job] = (row[2], row[3])

            result = pickle.load(open('%s/cache/schedule.pickle' % MEDIA_ROOT, 'rb'))

            if flag == 'weekly':
                if datetime.utcnow().date().isoweekday() == 4:
                    self.compose_msg(ppls[flag]['breakfast'], 'Breakfast', flag, ' to _Group Meeting_ tomorrow')
                    if result['this'][1] == 'ES':
                        self.compose_msg(ppls['monthly']['eterna'], 'Eterna Microphone Setup', flag, ' for _Eterna Open Group Meeting_ tomorrow. Please arrive *30 min* early. The instructions are <https://docs.google.com/document/d/1bh5CYBklIdZl65LJDsBffC8m8J_3jKf4FY1qiYjRIw8/edit|here>')
                elif datetime.utcnow().date().isoweekday() == 2:
                    if result['this'][1] == 'ES':
                        who = result['this'][2]
                        who_id = self.find_slack_id(who)
                        self.compose_msg(result['this'][2], 'Eterna Broadcast Posting', flag, ' Just a reminder for sending a description of your upcoming _Eterna Open Group Meeting_ to <%s> and <@%s> for releasing news on both DasLab Website and EteRNA broadcast.' % (SLACK['ADMIN_NAME'], self.find_slack_id(ppls['monthly']['eterna'])))
                        self.compose_msg(ppls['monthly']['eterna'], 'Eterna Broadcast Posting', flag, ' for _Eterna Open Group Meeting_. If _%s_ <@%s> hasn\'t send out descriptions, please ask him/her!' % (who, who_id))
                        self.msg_handles.append( (SLACK['ADMIN_NAME'], '', [{"fallback":'Reminder', "mrkdwn_in": ["text", "fields"], "color":"c28fdd", "text":'*LAB DUTY*: Just a reminder for posting news on lab website about the upcoming _Eterna Open Group Meeing_ on *%s* by _%s_ <@%s>.' % (result['this'][0], who, who_id)}]) )
                    elif result['this'][1] == 'JC':
                        who = result['this'][2]
                        who_id = self.find_slack_id(who)
                        self.compose_msg(result['this'][2], 'Journal Club Posting', flag, ' Just a reminder for posting your paper of choice for the upcoming _Journal Club_ to `#general`.')
                    else:
                        return


            elif flag == 'monthly':
                self.compose_msg(ppls[flag]['amazon'], 'Amazon Web Services', flag, '')
                self.compose_msg(ppls[flag]['website'], 'Website', flag, '')
                self.compose_msg(ppls[flag]['group meeting'], 'Meeting Scheduling', flag, '')
                self.compose_msg(ppls[flag]['birthday'], 'Birthday Celebrations', flag, '')

                day = datetime.utcnow().date()
                fields = []
                for ppl in Member.objects.filter(alumni=0).exclude(bday__isnull=True).order_by('bday'):
                    temp = datetime.strptime('%s/%s' % (day.year, ppl.bday), '%Y/%m/%d')
                    is_upcoming = (temp <= datetime.utcnow() + timedelta(days=60)) and (temp >= datetime.utcnow())
                    if day.month >= 10:
                        temp = datetime.strptime('%s/%s' % (day.year + 1, ppl.bday), '%Y/%m/%d')
                        is_upcoming = is_upcoming or ( (temp <= datetime.utcnow() + timedelta(days=60)) and (temp >= datetime.utcnow()) )
                    if is_upcoming:
                        fields.append({'title':ppl.full_name(), 'value':ppl.bday, 'short':True})
                if not fields: fields.append({'title': 'Nobody', 'value':'_within next 60 days_', 'short':True})

                birthday = ppls[flag]['birthday']
                who_main = self.find_slack_id(birthday[0])
                who_bkup = self.find_slack_id(birthday[1])
                send_to = '@' + who_main
                if DEBUG: send_to = SLACK['ADMIN_NAME']
                self.msg_handles.append( (send_to, '', [{"fallback":'Reminder', "mrkdwn_in": ["text", "fields"], "color":"ff912e", "text":'_Upcoming Birthdays_:', "fields":fields}]) )

                if datetime.utcnow().date().month == 10:
                    self.msg_handles.append( (SLACK['ADMIN_NAME'], '', [{"fallback":'Reminder', "mrkdwn_in": ["text", "fields"], "color":"3ed4e7", "text":'*REMINDER*: Renewal of `Dropbox` membership _annually_. Please check the payment status.'}]) )


            elif flag == 'quarterly':
                self.compose_msg(ppls[flag]['lab trips'], 'Lab Outing/Trips', flag, '')
                self.compose_msg(ppls[flag]['github'], 'Mailing, Slack, GitHub', flag, '')

            subprocess.check_call("rm %s/cache/duty.csv" % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
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
