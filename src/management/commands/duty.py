from datetime import datetime, timedelta
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.models import Member
from src.console import send_notify_slack, send_error_slack, find_slack_id
from src.dash import dash_schedule, dash_duty


class Command(BaseCommand):
    help = 'Send out individual Responsibility Reminder notifications in Slack.'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.msg_handles = []

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('interval', nargs='+', type=str, help='Interval, choose from (week, month, quarter).')


    def compose_msg(self, task_tuple, task_name, interval, alt_text):
        (who_main, _) = find_slack_id(task_tuple['main'])
        (who_bkup, _) = find_slack_id(task_tuple['backup'])
        if who_main:
            msg = '*LAB DUTY*: Just a reminder for the _%s_ task of `%s`%s. If you are unable to do so, please inform the ' % (interval, task_name, alt_text)
            if who_bkup and who_bkup != who_main:
                msg += 'backup person for this task: _%s_ <@%s>.' % (task_tuple['backup'], who_bkup)
            else:
                msg += 'site admin <@%s> since there is *NO* backup person for this task.' % SLACK['ADMIN_NAME']
            send_to = SLACK['ADMIN_NAME'] if DEBUG else '@' + who_main
            self.msg_handles.append( (send_to, '', [{"fallback": 'Reminder', "mrkdwn_in": ["text"], "color": "c28fdd", "text": msg }]) )
        else:
            self.msg_handles.append( (SLACK['ADMIN_NAME'], '', [{"fallback": 'Reminder', "mrkdwn_in": ["text"], "color": "ff912e", "text": '*WARNING*: No one [%s?] is primarily assigned for the duty of _%s_ check of `%s`. *NO* reminder sent.' % (task_tuple['main'], interval, task_name) }]) )


    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))

        if options['interval']:
            if options['interval'][0].endswith('ly'):
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
            result = dash_duty(0)
            ppls = result['ppls']
            result = dash_schedule(0)

            if flag == 'weekly':
                day_1 = (result['weekday'] - int(BOT['SLACK']['REMINDER']['DAY_BEFORE_REMINDER_1']))
                day_2 = (result['weekday'] - int(BOT['SLACK']['REMINDER']['DAY_BEFORE_REMINDER_2']))
                if day_1 < 0: day_1 += 7
                if day_2 < 0: day_2 += 7

                if datetime.utcnow().date().isoweekday() == day_1:
                    if result['this']['type'] != 'N/A':
                        if BOT['SLACK']['DUTY']['MONTH']['MSG_BREAKFAST']:
                            self.compose_msg(ppls[flag]['breakfast'], 'Breakfast', flag, ' to _Group Meeting_ tomorrow')
                    if result['this']['type'] == 'ES':
                        if BOT['SLACK']['DUTY']['ETERNA']['MSG_MIC']:
                            self.compose_msg(ppls['monthly']['eterna'], 'Eterna Microphone Setup', flag, ' for the upcoming _Eterna Open Group Meeting_. Please arrive *30 min* early. The instructions are <https://docs.google.com/document/d/1bh5CYBklIdZl65LJDsBffC8m8J_3jKf4FY1qiYjRIw8/edit|here>')

                elif datetime.utcnow().date().isoweekday() == day_2:
                    offset = int(BOT['SLACK']['REMINDER']['DAY_BEFORE_REMINDER_2'])
                    year = (datetime.utcnow() + timedelta(days=offset)).date().year
                    date = datetime.strptime("%s %s" % (dash_schedule(0)['this']['date'], year), '%b %d %Y')
                    if (datetime.utcnow() + timedelta(days=offset)).date() != date.date():
                        (who_id, _) = find_slack_id(ppls['weekly']['group meeting']['main'])
                        send_to = SLACK['ADMIN_NAME'] if DEBUG else '@' + who_id
                        send_notify_slack(send_to, '', [{"fallback": 'ERROR', "mrkdwn_in": ["text"], "color": "warning", "text": 'Mismatch in Schedule Spreadsheet date. It seems to be not up-to-date. Please fix the Spreadsheet immediately!'}])

                    if result['this']['type'] == 'ES':
                        who = result['this']['who']
                        (who_id, _) = find_slack_id(who)
                        send_to = SLACK['ADMIN_NAME'] if DEBUG else '@' + who_id

                        if BOT['SLACK']['REMINDER']['ES']['REMINDER_2']:
                            (who_id2, _) = find_slack_id(ppls['monthly']['eterna']['main'])
                            self.msg_handles.append( (send_to, '', [{"fallback": 'Reminder', "mrkdwn_in": ["text", "fields"], "color": "c28fdd", "text": '*LAB DUTY*: Just a reminder for sending a description of your upcoming _Eterna Open Group Meeting_ to <%s> and <@%s> for releasing news on both DasLab Website and EteRNA broadcast.' % (SLACK['ADMIN_NAME'], who_id2)}]) )
                        if BOT['SLACK']['DUTY']['ETERNA']['MSG_BROADCAST']:
                            self.compose_msg(ppls['monthly']['eterna'], 'Eterna Broadcast Posting', flag, ' for _Eterna Open Group Meeting_. If _%s_ <@%s> hasn\'t send out descriptions, please ask him/her!' % (who, who_id))
                        if BOT['SLACK']['DUTY']['ETERNA']['MSG_NEWS']:
                            (who_id, _) = find_slack_id(ppls['monthly']['website']['main'])
                            send_to = SLACK['ADMIN_NAME'] if DEBUG else '@' + who_id
                            self.msg_handles.append( (send_to, '', [{"fallback": 'Reminder', "mrkdwn_in": ["text", "fields"], "color": "c28fdd", "text": '*LAB DUTY*: Just a reminder for posting news on lab website about the upcoming _Eterna Open Group Meeing_ on *%s* by _%s_ <@%s>.' % (result['this']['date'], who, who_id)}]) )
                    elif result['this']['type'] == 'JC':
                        if BOT['SLACK']['REMINDER']['JC']['REMINDER_2']:
                            who = result['this']['who']
                            (who_id, _) = find_slack_id(who)
                            send_to = SLACK['ADMIN_NAME'] if DEBUG else '@' + who_id
                            self.msg_handles.append( (send_to, '', [{"fallback": 'Reminder', "mrkdwn_in": ["text", "fields"], "color": "c28fdd", "text": '*LAB DUTY*: Just a reminder for posting your paper of choice for the upcoming _Journal Club_ to `#general`.'}]) )
                    else:
                        return
                elif datetime.utcnow().date().isoweekday() == result['weekday']:
                    if BOT['SLACK']['DUTY']['MONTH']['MSG_SCHEDULE']:
                        self.compose_msg(ppls[flag]['group meeting'], 'Meeting Scheduling', flag, ' (move current down to bottom, and move next up top)')
                else:
                    return


            elif flag == 'monthly':
                if BOT['SLACK']['DUTY']['MONTH']['MSG_AWS']:
                    self.compose_msg(ppls[flag]['amazon'], 'Amazon Web Services', flag, '')
                if BOT['SLACK']['DUTY']['MONTH']['MSG_WEBSITE']:
                    self.compose_msg(ppls[flag]['website'], 'Website', flag, '')

                if BOT['SLACK']['DUTY']['MONTH']['MSG_BDAY']:
                    self.compose_msg(ppls[flag]['birthday'], 'Birthday Celebrations', flag, '')

                    day = datetime.utcnow().date()
                    fields = []
                    for ppl in Member.objects.filter(is_alumni=0).exclude(bday__isnull=True).order_by('bday'):
                        temp = datetime.strptime('%s/%s' % (day.year, ppl.bday), '%Y/%m/%d')
                        is_upcoming = (temp <= datetime.utcnow() + timedelta(days=60)) and (temp >= datetime.utcnow())
                        if day.month >= 10:
                            temp = datetime.strptime('%s/%s' % (day.year + 1, ppl.bday), '%Y/%m/%d')
                            is_upcoming = is_upcoming or ( (temp <= datetime.utcnow() + timedelta(days=60)) and (temp >= datetime.utcnow()) )
                        if is_upcoming:
                            fields.append({'title': ppl.full_name(), 'value': ppl.bday, 'short': True})
                    if not fields: fields.append({'title': 'Nobody', 'value': '_within next 60 days_', 'short': True})

                    birthday = ppls[flag]['birthday']
                    (who_main, _) = find_slack_id(birthday['main'])
                    (who_bkup, _) = find_slack_id(birthday['backup'])
                    send_to = SLACK['ADMIN_NAME'] if DEBUG else '@' + who_main
                    self.msg_handles.append( (send_to, '', [{"fallback": 'Reminder', "mrkdwn_in": ["text", "fields"], "color": "ff912e", "text": '_Upcoming Birthdays_:', "fields": fields}]) )

                if datetime.utcnow().date().month == 10:
                    (who_id, _) = find_slack_id(ppls['quarterly']['github']['main'])
                    send_to = SLACK['ADMIN_NAME'] if DEBUG else '@' + who_id
                    self.msg_handles.append( (send_to, '', [{"fallback": 'Reminder', "mrkdwn_in": ["text", "fields"], "color": "3ed4e7", "text": '*REMINDER*: Renewal of `Dropbox` membership _annually_. Please renew and check the payment status.'}]) )
                    self.msg_handles.append( (send_to, '', [{"fallback": 'Reminder', "mrkdwn_in": ["text", "fields"], "color": "3ed4e7", "text": '*REMINDER*: Renewal of `GitHub` membership _annually_. Please renew and check the payment status.'}]) )
                elif datetime.utcnow().date().month == 8:
                    (who_id, _) = find_slack_id(ppls[flag]['amazon']['main'])
                    send_to = SLACK['ADMIN_NAME'] if DEBUG else '@' + who_id
                    self.msg_handles.append( (send_to, '', [{"fallback": 'Reminder', "mrkdwn_in": ["text", "fields"], "color": "3ed4e7", "text": '*REMINDER*: Renewal of `AWS` reserved instances [all upfront] _annually_. Please renew and check the payment status.'}]) )


            elif flag == 'quarterly':
                if BOT['SLACK']['DUTY']['QUARTER']['MSG_TRIP']:
                    self.compose_msg(ppls[flag]['lab trips'], 'Lab Outing / Trips', flag, '')
                if BOT['SLACK']['DUTY']['QUARTER']['MSG_GIT']:
                    self.compose_msg(ppls[flag]['github'], 'Mailing / Slack / GitHub', flag, '')

        except Exception:
            print traceback.format_exc()
            send_error_slack(traceback.format_exc(), 'Send Duty Reminders', ' '.join(sys.argv), 'log_cron_duty.log')
            self.stdout.write("Finished with \033[41mERROR\033[0m!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(1)

        else:
            for h in self.msg_handles:
                send_notify_slack(*h)
                if '@' in h[0]:
                    self.stdout.write('\033[92mSUCCESS\033[0m: PM\'ed duty reminder to \033[94m%s\033[0m in Slack.' % h[0])

        if (not DEBUG) and len(self.msg_handles):
            send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback": 'SUCCESS', "mrkdwn_in": ["text"], "color": "good", "text": '*SUCCESS*: Scheduled %s *Duty Reminder* finished @ _%s_\n' % (flag, time.ctime())}])
        self.stdout.write("Finished with \033[92mSUCCESS\033[0m!")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
