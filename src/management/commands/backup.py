import os
import subprocess
import sys
import tarfile
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.console import get_date_time, get_backup_stat, send_notify_emails, send_notify_slack, send_error_slack


class Command(BaseCommand):
    help = 'Backups MySQL database, static files, Apache2 settings and config settings to local backup/ folder. Existing backup files will be overwritten.'

    def add_arguments(self, parser):
        parser.add_argument('--item', nargs='+', type=str, help='List of backup itmes, choose from (\'apache\', \'config\', \'mysql\', \'static\')')

    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))

        if options['item']:
            is_apache = 'apache' in options['item']
            is_config = 'config' in options['item']
            is_mysql = 'mysql' in options['item']
            is_static = 'static' in options['item']
        else:
            is_apache, is_config, is_mysql, is_static = True, True, True, True

        flag = False
        if is_mysql:
            t = time.time()
            self.stdout.write('#1: Backing up MySQL database...')
            try:
                subprocess.check_call(
                    'mysqldump --quick %s -u %s -p%s > %s/backup/backup_mysql' % (env.db()['NAME'], env.db()['USER'], env.db()['PASSWORD'], MEDIA_ROOT),
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                tarfile.open('%s/backup/backup_mysql.tgz' % MEDIA_ROOT, 'w:gz').add('%s/backup/backup_mysql' % MEDIA_ROOT, arcname='backup_mysql')
                os.remove('%s/backup/backup_mysql' % MEDIA_ROOT)
            except Exception:
                send_error_slack(traceback.format_exc(), 'Backup MySQL Database', ' '.join(sys.argv), 'log_cron_backup.log')
                flag = True
            else:
                self.stdout.write('    \033[92mSUCCESS\033[0m: \033[94mMySQL\033[0m database dumped.')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t))


        if is_static:
            t = time.time()
            self.stdout.write('#2: Backing up static files...')
            try:
                tarfile.open('%s/backup/backup_static.tgz' % MEDIA_ROOT, 'w:gz').add('%s/data' % MEDIA_ROOT, arcname='data')
            except Exception:
                send_error_slack(traceback.format_exc(), 'Backup Static Files', ' '.join(sys.argv), 'log_cron_backup.log')
                flag = True
            else:
                self.stdout.write('    \033[92mSUCCESS\033[0m: \033[94mstatic\033[0m files synced.')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t))


        if is_apache:
            t = time.time()
            self.stdout.write('#3: Backing up apache2 settings...')
            try:
                pass
                # tarfile.open('%s/backup/backup_apache2.tgz' % MEDIA_ROOT, 'w:gz').add('/etc/apache2', arcname='apache2')
            except Exception:
                send_error_slack(traceback.format_exc(), 'Backup Apache2 Settings', ' '.join(sys.argv), 'log_cron_backup.log')
                flag = True
            else:
                self.stdout.write('    \033[92mSUCCESS\033[0m: \033[94mapache2\033[0m settings saved.')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t))


        if is_config:
            t = time.time()
            self.stdout.write('#4: Backing up config settings...')
            try:
                tarfile.open('%s/backup/backup_config.tgz' % MEDIA_ROOT, 'w:gz').add('%s/config' % MEDIA_ROOT, arcname='config')
            except Exception:
                send_error_slack(traceback.format_exc(), 'Backup Config Settings', ' '.join(sys.argv), 'log_cron_backup.log')
                flag = True
            else:
                self.stdout.write('    \033[92mSUCCESS\033[0m: \033[94mconfig\033[0m settings saved.')
            self.stdout.write('Time elapsed: %.1f s.\n' % (time.time() - t))


        if flag:
            self.stdout.write('Finished with errors!')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t0))
            sys.exit(1)
        else:
            if DEBUG:
                self.stdout.write('\033[94m Backed up locally. \033[0m')
            else:
                (t_cron, d_cron, t_now) = get_date_time('backup')
                local_list = subprocess.Popen(
                    'ls -gh %s/backup/*.*gz' % MEDIA_ROOT,
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                ).communicate()[0].strip().split()
                html = 'File\t\t\t\tTime\t\t\t\tSize\n\n'
                for i in xrange(0, len(local_list), 8):
                    html += '%s\t\t%s %s, %s\t\t%s\n' % (local_list[i + 7], local_list[i + 4], local_list[i + 5], local_list[i + 6], local_list[i + 3])

                if IS_SLACK:
                    if (not DEBUG) and BOT['SLACK']['ADMIN']['MSG_BACKUP']:
                        send_notify_slack(
                            SLACK['ADMIN_NAME'],
                            '',
                            [{
                                'fallback': 'SUCCESS',
                                'mrkdwn_in': ['text'],
                                'color': PATH.PALETTE['green'],
                                'text': '*SUCCESS*: Scheduled weekly *Backup* finished @ _%s_\n' % time.ctime(),
                            }]
                        )
                        # send_notify_slack(SLACK['ADMIN_NAME'], '>```%s```\n' % html, '')
                else:
                    send_notify_emails(
                        '{%s} SYSTEM: Weekly Backup Notice' % env('SERVER_NAME'),
                        'This is an automatic email notification for the success of scheduled weekly backup of the %s Website database and static contents.\n\nThe crontab job is scheduled at %s (UTC) on every %sday.\n\nThe last system backup was performed at %s (PDT).\n\n%s\n\n%s Website Admin\n' % (env('SERVER_NAME'), t_cron, d_cron, t_now, html, env('SERVER_NAME'))
                    )
                    self.stdout.write('Admin email (Weekly Backup Notice) sent.')
            get_backup_stat()
            self.stdout.write('Admin Backup Statistics refreshed.')

            self.stdout.write('All done successfully!')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t0))

