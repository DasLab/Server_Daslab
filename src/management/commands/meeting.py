from datetime import datetime, timedelta
import requests
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.models import FlashSlide
from src.console import send_notify_emails, send_notify_slack, send_error_slack, find_slack_id
from src.dash import dash_schedule, dash_duty


class Command(BaseCommand):
    help = 'Parses Group Meeting schedule, create and share Google Presentation, add to FlashSlide database table, send out Group Meeting Reminder and individual notifications in Slack.'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.types = {
            'ES': 'EteRNA Special',
            'GM': 'Group Meeting',
            'JC': 'Journal Club',
            'FS': 'Flash Slides',
        }
        self.msg_handles = []

    def send_to(id, channel=False):
        if DEBUG:
            return SLACK['ADMIN_NAME']
        else:
            prefix = '#' if channel else '@'
            return '%s%s' % (prefix, id)

    def slack_match_names(name):
        if '/' in name or '&' in name:
            return name.replace('/', '*|*').replace('&', '*|*').replace(' ', '').split('*|*')
        elif name.strip() and name != '-':
            return [name]
        else:
            return []

    def slack_id_error(sunet_id, name, role):
        if sunet_id == 'none':
            msg = 'not found'
        elif sunet_id == 'ambiguous':
            msg = 'is ambiguate (more than 1 match)'
        else:
            msg = 'not available in database'
        self.stdout.write('\033[41mERROR\033[0m: %s (\033[94m%s\033[0m) %s.' % (role, name, msg))


    def handle(self, *args, **options):
        if not BOT['SLACK']['IS_FLASH_SETUP']:
            return
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))
        flag_mismatch = False

        try:
            result = dash_duty(0)
            ppls = result['ppls']
            result = dash_schedule(0)
            offset_1 = int(BOT['SLACK']['REMINDER']['DAY_BEFORE_REMINDER_1'])
            offset_2 = int(BOT['SLACK']['REMINDER']['DAY_BEFORE_REMINDER_2'])
            day_1 = (result['weekday'] - offset_1) % 7
            today = datetime.utcnow()
            if today.date().isoweekday() % 7 != day_1:
                return

            meeting_date = today + timedelta(days=offset_1)
            year = meeting_date.date().year
            target_date_str = '%s %s' % (result['this']['date'], year)
            target_date = datetime.strptime(target_date_str, '%b %d %Y')

            if result['this']['type'] == 'N/A':
                msg_this = 'Hi all,\n\nThis is a reminder that there will be *`NO Meeting`* this week'
                if result['this']['note']:
                    msg_this += ' due to: _%s_.' % result['this']['note']
                else:
                    msg_this += '.'
                self.msg_handles.append((
                    self.send_to('general', channel=True),
                    '',
                    [{
                        'fallback': 'Reminder',
                        'mrkdwn_in': ['text'],
                        'color': 'good',
                        'title': 'Group Meeting Reminder',
                        'text': msg_this,
                        'thumb_url': 'https://daslab.stanford.edu/site_media/images/group/logo_bot.jpg',
                    }]
                ))
                self.stdout.write('\033[92mSUCCESS\033[0m: Google Presentation skipped (N/A for this week: \033[94m%s\033[0m).' % target_date_str)
            else:
                type_this = self.types[result['this']['type']]
                if meeting_date.date() != target_date.date():
                    (who_id, _) = find_slack_id(ppls['weekly']['group meeting']['main'])
                    send_notify_slack(
                        self.send_to(who_id),
                        '',
                        [{
                            'fallback': 'ERROR',
                            'mrkdwn_in': ['text'],
                            'color': 'warning',
                            'text': 'Mismatch in Schedule Spreadsheet date. It seems to be not up-to-date.\nFlash Slide has *`NOT`* been setup yet for this week! Please investigate and fix the setup immediately.',
                        }]
                    )
                    flag_mismatch = True
                    sys.exit(1)

                title = 'Flash Slides: %s' % target_date_str
                access_token = requests.post(
                    'https://www.googleapis.com/oauth2/v3/token?refresh_token=%s&client_id=%s&client_secret=%s&grant_type=refresh_token' % (
                        DRIVE['REFRESH_TOKEN'], DRIVE['CLIENT_ID'], DRIVE['CLIENT_SECRET']
                    )
                ).json()['access_token']
                temp = requests.post(
                    'https://www.googleapis.com/drive/v2/files/%s/copy?access_token=%s' % (DRIVE['TEMPLATE_PRESENTATION_ID'], access_token),
                    json={'title': title}
                )
                ppt_id = temp.json()['id']
                temp = requests.post(
                    'https://www.googleapis.com/drive/v2/files/%s/permissions?sendNotificationEmails=false&access_token=%s' % (ppt_id, access_token),
                    json={
                        'role': 'writer',
                        'type': 'group',
                        'value': 'das-lab@googlegroups.com',
                    }
                )
                if temp.status_code != 200:
                    self.stdout.write('\033[41mERROR\033[0m: Google Presentation (\033[94m%s\033[0m) created but NOT shared.' % ppt_id)
                    if IS_SLACK:
                        (who_id, _) = find_slack_id(ppls['weekly']['flash slide']['main'])
                        send_notify_slack(
                            self.send_to(who_id),
                            '',
                            [{
                                'fallback': 'ERROR',
                                'mrkdwn_in': ['text'],
                                'color': 'warning',
                                'text': 'FlashSlide was created but failed on sharing to the group.\nFlash Slide setup is *`NOT`* complete! Please investigate and fix the setup immediately.',
                            }]
                        )
                        send_error_slack(temp.json(), 'Group Meeting Setup', ' '.join(sys.argv), 'log_cron_cache.log')
                else:
                    self.stdout.write('\033[92mSUCCESS\033[0m: Google Presentation (\033[94m%s\033[0m) created and shared.' % ppt_id)

                flash_slide = FlashSlide(date=target_date, link='https://docs.google.com/presentation/d/%s/edit#slide=id.p' % ppt_id)
                flash_slide.save()
                self.stdout.write('\033[92mSUCCESS\033[0m: Google Presentation (\033[94m%s\033[0m) saved in MySQL.' % ppt_id)

                note = result['this']['note'].lower().replace(' ', '')
                name = result['this']['who']
                ids = []
                names = slack_match_names(name)

                if name:
                    for name in names:
                        (who_id, sunet_id) = find_slack_id(name)
                        if note == 'endofrotationtalk' and BOT['SLACK']['REMINDER']['ROT']['REMINDER_1']:
                            if GROUP.find_type(sunet_id) == 'roton':
                                msg_who = 'Just a reminder: Please send your presentation to %s (site admin) for `archiving` *after* your presentation this _%s_.' % (SLACK['ADMIN_NAME'], datetime.strftime(target_date, '%A'))
                                ids.append('_' + name + '_ <@' + who_id + '>')
                                self.msg_handles.append((
                                    self.send_to(who_id),
                                    '',
                                    [{
                                        'fallback': 'Reminder',
                                        'mrkdwn_in': ['text'],
                                        'color': 'good',
                                        'text': msg_who,
                                    }]
                                ))
                            else:
                                self.slack_id_error(sunet_id, name, 'rotation student')
                        elif GROUP.find_type(sunet_id) in ['admin', 'group', 'alumni', 'other']:
                            ids.append('_' + name + '_ <@' + who_id + '>')
                        else:
                            ids.append('_%s_' % name)
                else:
                    ids = ['_(None)_']

                (who_id, _) = find_slack_id(ppls['monthly']['website']['main'])
                send_to = self.send_to(who_id)
                reminder_date_str = datetime.strftime(target_date, '%b %d %Y (%a)')
                item = ''
                if (note == 'endofrotationtalk' and
                    BOT['SLACK']['REMINDER']['ROT']['REMINDER_ADMIN']):
                    item = 'RotationStudent'
                elif (result['this']['type'] == 'JC' and
                    BOT['SLACK']['REMINDER']['JC']['REMINDER_ADMIN']):
                    item = 'JournalClub'
                elif (result['this']['type'] == 'ES' and
                    BOT['SLACK']['REMINDER']['ES']['REMINDER_ADMIN']):
                    item = 'EternaYoutube'
                if item:
                    self.msg_handles.append((
                        send_to, '',
                        [{
                            'fallback': 'REMINDER',
                            'mrkdwn_in': ['text'],
                            'color': 'warning',
                            'text': '*REMINDER*: Add *%s* entry for _%s_.' % (item, reminder_date_str),
                        }]
                    ))

                send_to = self.send_to('general', channel=True)
                super_prefix = '*Extended/Super* ' if result['this']['type'] == 'FS' else ''
                self.msg_handles.append((
                    send_to, '',
                    [{
                        'fallback': 'Reminder',
                        'mrkdwn_in': ['text', 'fields'],
                        'color': 'good',
                        'title': 'Group Meeting Reminder',
                        'text': 'Hi all,\n\nThis is a reminder that group meeting will be %s*`%s`* for this week.\n' % (super_prefix, type_this),
                        'thumb_url': 'https://daslab.stanford.edu/site_media/images/group/logo_bot.jpg',
                        'fields': [
                            {
                                'title': 'Date',
                                'value': '_%s_' % reminder_date_str,
                                'short': True,
                            },
                            {
                                'title': 'Time & Place',
                                'value': '_%s @ %s_' % (result['time']['start'], result['place']),
                                'short': True,
                            },
                            {
                                'title': 'Type',
                                'value': '`%s`' % type_this,
                                'short': True,
                            }, {
                                'title': 'Presenter',
                                'value': '%s' % ', \n'.join(ids),
                                'short': True,
                            }
                        ],
                    }]
                ))
                self.msg_handles.append((
                    send_to, '',
                    [{
                        'fallback': '%s' % title,
                        'mrkdwn_in': ['text'],
                        'color': 'warning',
                        'title': '%s' % title,
                        'text': '*<https://docs.google.com/presentation/d/%s/edit#slide=id.p>*\nA <https://daslab.stanford.edu/group/flash_slide/|full list> of Flash Slide links is available on the DasLab Website.' % ppt_id,
                    }]
                ))

            if (result['last']['note'].lower().replace(' ', '') == 'endofrotationtalk' and
                BOT['SLACK']['REMINDER']['ROT']['REMINDER_2']):
                (who_id, _) = find_slack_id(ppls['quarterly']['github']['main'])
                self.msg_handles.append((
                    self.send_to(who_id),
                    '',
                    [{
                        'fallback': 'REMINDER',
                        'mrkdwn_in': ['text'],
                        'color': 'warning',
                        'text': '*REMINDER*: Revoke permissions (_Group Website_ and _Slack Membership_) of recent finished *RotationStudent*.',
                    }]
                ))


            if result['next']['type'] == 'N/A':
                msg_next = 'For next week, there will be *`NO Meeting`*'
                if result['next']['note']:
                    msg_next += ' due to: _%s_.' % result['next']['note']
                else:
                    msg_next += '.'
                self.msg_handles.append((
                    self.send_to('general', channel=True),
                    '',
                    [{
                        'fallback': 'Reminder',
                        'mrkdwn_in': ['text'],
                        'color': '439fe0',
                        'text': msg_next,
                    }]
                ))
            else:
                type_next = self.types[result['next']['type']]
                year = (today + timedelta(days=(offset_1 + 7))).date().year
                next_date = datetime.strptime('%s %s' % (result['next']['date'], year), '%b %d %Y')
                next_date_str = datetime.strftime(next_date, '_%A_ (*%b %d*)')

                day_2 = (today + timedelta(days=(offset_1 + 7 - offset_2))).date()
                day_2_str = datetime.strftime(day_2, '_%A_ (*%b %d*)')
                msg_who = 'Just a reminder that you are up for `%s` *next* %s.\n' % (type_next, next_date_str)
                if (result['next']['type'] == 'JC' and
                    BOT['SLACK']['REMINDER']['JC']['REMINDER_1']):
                    msg_who += ' Please post your paper of choice to the group `#general` channel by *next* %s.\n' % day_2_str
                elif (result['next']['type'] == 'ES' and
                    BOT['SLACK']['REMINDER']['ES']['REMINDER_1']):
                    msg_who += ' Please post a brief description of the topic to the group `#general` channel by *next* %s to allow time for releasing news on both DasLab Website and EteRNA broadcast.\n' % day_2_str

                name = result['next']['who']
                ids = []
                names = slack_match_names(name)

                if name:
                    for name in names:
                        (who_id, sunet_id) = find_slack_id(name)
                        if GROUP.find_type(sunet_id) != 'unknown':
                            ids.append('_' + name + '_ <@' + who_id + '>')

                            if ((result['next']['type'] == 'JC' and BOT['SLACK']['REMINDER']['JC']['REMINDER_1']) or
                                (result['next']['type'] == 'ES' and BOT['SLACK']['REMINDER']['ES']['REMINDER_1']) or
                                (result['next']['type'] == 'GM' and
                                    (BOT['SLACK']['REMINDER']['JC']['REMINDER_1'] or BOT['SLACK']['REMINDER']['ES']['REMINDER_1'] or BOT['SLACK']['REMINDER']['ROT']['REMINDER_1'])
                                    )
                                ):
                                self.msg_handles.append((
                                    self.send_to(who_id),
                                    '',
                                    [{
                                        'fallback': 'Reminder',
                                        'mrkdwn_in': ['text'],
                                        'color': 'good',
                                        'text': msg_who,
                                    }]
                                ))
                            else:
                                self.slack_id_error(sunet_id, name, 'member')
                        else:
                            ids.append('_%s_' % name)
                else:
                    ids = ['_(None)_']

                send_to = self.send_to('general', channel=True)
                self.msg_handles.append((
                    send_to, '',
                    [{
                        'fallback': 'Reminder',
                        'mrkdwn_in': ['text', 'fields'],
                        'color': '439fe0',
                        'text': 'For next week: \n',
                        'thumb_url': 'https: //daslab.stanford.edu/site_media/images/group/logo_bot.jpg',
                        'fields': [
                            {
                                'title': 'Date',
                                'value': '_%s_' % datetime.strftime(next_date, '%b %d %Y (%a)'),
                                'short': True,
                            },
                            {
                                'title': 'Time & Place',
                                'value': '_%s @ %s_' % (result['time']['start'], result['place']),
                                'short': True,
                            },
                            {
                                'title': 'Type',
                                'value': '`%s`' % type_next,
                                'short': True,
                            },
                            {
                                'title': 'Presenter',
                                'value': '%s' % ', \n'.join(ids),
                                'short': True,
                            }
                        ],
                    }]
                ))

            (who_id, _) = find_slack_id(ppls['weekly']['group meeting']['main'])
            self.msg_handles.append((
                send_to, '',
                [{
                    'fallback': 'Reminder',
                    'mrkdwn_in': ['text'],
                    'color': 'danger',
                    'text': 'The <https://daslab.stanford.edu/group/schedule/|full schedule> is available on the DasLab Website. For questions regarding the schedule, please contact <@%s>. Thanks for your attention.\n\nSite Admin: <%s>' % (who_id, SLACK['ADMIN_NAME']),
                }]
            ))

        except Exception:
            if flag_mismatch:
                return
            send_error_slack(traceback.format_exc(), 'Group Meeting Setup', ' '.join(sys.argv), 'log_cron_meeting.log')

            if result['this']['type'] != 'N/A':
                FlashSlide.objects.get(date=target_date).delete()
                requests.delete('https://www.googleapis.com/drive/v2/files/%s/?access_token=%s' % (ppt_id, access_token))
                self.stdout.write('\033[92mSUCCESS\033[0m: Google Presentation (\033[94m%s\033[0m) deleted.' % ppt_id)
                self.stdout.write('\033[92mSUCCESS\033[0m: Google Presentation (\033[94m%s\033[0m) removed in MySQL.' % ppt_id)

            if IS_SLACK:
                (who_id, _) = find_slack_id(ppls['weekly']['flash slide']['main'])
                send_notify_slack(
                    self.send_to(who_id),
                    '',
                    [{
                        'fallback': 'ERROR',
                        'mrkdwn_in': ['text'],
                        'color': 'warning',
                        'text': 'FlashSlide table in MySQL database, presentation in Google Drive, and posted messages in Slack are rolled back.\nFlash Slide has *`NOT`* been setup yet for this week! Please investigate and fix the setup immediately.',
                    }]
                )
            else:
                send_notify_emails(
                    '{%s} ERROR: Weekly Meeting Setup' % env('SERVER_NAME'),
                    'This is an automatic email notification for the failure of scheduled weekly flash slides setup. The following error occurred:\n\n%s\n\n%s\n\nFlashSlide table in MySQL database, presentation in Google Drive, and posted messages in Slack are rolled back.\n\n** Flash Slide has NOT been setup yet for this week! Please investigate and fix the setup immediately.\n\n%s Website Admin' % (ts, err, env('SERVER_NAME'))
                )

            self.stdout.write('Finished with \033[41mERROR\033[0m!')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t0))
            sys.exit(1)

        else:
            for h in self.msg_handles:
                send_notify_slack(*h)
                if '@' in h[0]:
                    self.stdout.write('\033[92mSUCCESS\033[0m: PM\'ed reminder to \033[94m%s\033[0m in Slack.' % h[0])
            self.stdout.write('\033[92mSUCCESS\033[0m: Google Presentation posted in Slack.')
            self.stdout.write('\033[92mSUCCESS\033[0m: Meeting Reminder posted in Slack.')

        if (not DEBUG):
            (who_id, _) = find_slack_id(ppls['weekly']['flash slide']['main'])
            send_notify_slack(
                self.send_to(who_id),
                '',
                [{
                    'fallback': 'SUCCESS',
                    'mrkdwn_in': ['text'],
                    'color': 'good',
                    'text': '*SUCCESS*: Scheduled weekly *Flash Slides Setup* finished @ _%s_. Please also paste the link in the Schedule Spreadsheet.\n' % time.ctime(),
                }]
            )
        self.stdout.write('Finished with \033[92mSUCCESS\033[0m!')
        self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t0))

