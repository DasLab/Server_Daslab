from datetime import datetime, timedelta
import os.path
import subprocess
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.models import SlackMessage
from src.console import send_notify_emails, send_notify_slack, send_error_slack


class Command(BaseCommand):
    help = 'Send email to admin of weekly aggregated errors and gzip the log_cron.log file.'

    def handle(self, *args, **options):
        if not BOT['SLACK']['IS_REPORT']:
            return
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))

        try:
            if os.path.exists('%s/cache/log_alert_admin.log' % MEDIA_ROOT):
                lines = open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'r').readlines()
                lines = ''.join(lines)
                if (not IS_SLACK):
                    send_notify_emails(
                        '{%s} SYSTEM: Weekly Error Report' % env('SERVER_NAME'),
                        'This is an automatic email notification for the aggregated weekly error report. The following error occurred:\n\n\n%s\n\n%s Website Admin' % (lines, env('SERVER_NAME'))
                    )
                    open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'w').write('')
                    self.stdout.write('\033[92mSUCCESS\033[0m: All errors were sent to \033[94mEmail\033[0m. Log cleared.')
                else:
                    self.stdout.write('\033[92mSUCCESS\033[0m: All errors were reported to \033[94mSlack\033[0m already, nothing to do.')

            if os.path.exists('%s/cache/log_cron.log' % MEDIA_ROOT):
                subprocess.check_call(
                    'gzip -f %s/cache/log_cron.log' % MEDIA_ROOT,
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                self.stdout.write('\033[92mSUCCESS\033[0m: \033[94mlog_cron.log\033[0m gzipped.')
            else:
                self.stdout.write('\033[92mSUCCESS\033[0m: \033[94mlog_cron.log\033[0m not exist, nothing to do.')

            msgs = SlackMessage.objects.filter(
                date__lte=(datetime.utcnow() - timedelta(days=KEEP_BACKUP)).date()
            )
            for msg in msgs:
                msg.delete()

        except Exception:
            send_error_slack(traceback.format_exc(), 'Weekly Error Report', ' '.join(sys.argv), 'log_cron_report.log')
            self.stdout.write('Finished with \033[41mERROR\033[0m!')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t0))
            sys.exit(1)

        if (not DEBUG) and BOT['SLACK']['ADMIN']['MSG_REPORT']:
            send_notify_slack(
                SLACK['ADMIN_NAME'],
                '',
                [{
                    'fallback': 'SUCCESS',
                    'mrkdwn_in': ['text'],
                    'color': PATH.PALETTE['green'],
                    'text': '*SUCCESS*: Scheduled weekly *Report* finished @ _%s_\n' % time.ctime(),
                }]
            )
        self.stdout.write('Finished with \033[92mSUCCESS\033[0m!')
        self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t0))
