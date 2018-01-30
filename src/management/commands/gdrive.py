import datetime
import subprocess
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.console import get_date_time, get_backup_stat, send_notify_emails, send_notify_slack, send_error_slack


class Command(BaseCommand):
    help = 'Uploads MySQL database, static files, Apache2 settings and config settings from local backup/ folder to Google Drive, and deletes expired backup files in Google Drive. Uploaded files will be named with date.'

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

        d = time.strftime('%Y%m%d')  # datetime.datetime.now().strftime('%Y%m%d')
        gdrive_dir = 'echo' if DEBUG else 'cd %s' % APACHE_ROOT
        prefix = '_DEBUG' if DEBUG else ''

        flag = False
        if is_mysql:
            t = time.time()
            self.stdout.write('#1: Uploading MySQL database...')
            try:
                subprocess.check_call(
                    '%s && drive upload -f %s/backup/backup_mysql.tgz -t %s_%s_mysql%s.tgz' % (gdrive_dir, MEDIA_ROOT, env('SERVER_NAME'), d, prefix),
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
            except subprocess.CalledProcessError:
                send_error_slack(traceback.format_exc(), 'Upload MySQL Database', ' '.join(sys.argv), 'log_cron_gdrive.log')
                flag = True
            else:
                self.stdout.write('    \033[92mSUCCESS\033[0m: \033[94mMySQL\033[0m database uploaded.')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t))


        if is_static:
            t = time.time()
            self.stdout.write('#2: Uploading static files...')
            try:
                subprocess.check_call(
                    '%s && drive upload -f %s/backup/backup_static.tgz -t %s_%s_static%s.tgz' % (gdrive_dir, MEDIA_ROOT, env('SERVER_NAME'), d, prefix),
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
            except subprocess.CalledProcessError:
                send_error_slack(traceback.format_exc(), 'Upload Static Files', ' '.join(sys.argv), 'log_cron_gdrive.log')
                flag = True
            else:
                self.stdout.write('    \033[92mSUCCESS\033[0m: \033[94mstatic\033[0m files uploaded.')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t))


        if is_apache:
            t = time.time()
            self.stdout.write('#3: Uploading apache2 settings...')
            try:
                subprocess.check_call(
                    '%s && drive upload -f %s/backup/backup_apache.tgz -t %s_%s_apache%s.tgz' % (gdrive_dir, MEDIA_ROOT, env('SERVER_NAME'), d, prefix),
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
            except subprocess.CalledProcessError:
                send_error_slack(traceback.format_exc(), 'Upload Apache2 Settings', ' '.join(sys.argv), 'log_cron_gdrive.log')
                flag = True
            else:
                self.stdout.write('    \033[92mSUCCESS\033[0m: \033[94mapache2\033[0m settings uploaded.')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t))


        if is_config:
            t = time.time()
            self.stdout.write('#4: Uploading config settings...')
            try:
                subprocess.check_call(
                    '%s && drive upload -f %s/backup/backup_config.tgz -t %s_%s_config%s.tgz' % (gdrive_dir, MEDIA_ROOT, env('SERVER_NAME'), d, prefix),
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
            except subprocess.CalledProcessError:
                send_error_slack(traceback.format_exc(), 'Upload Config Settings', ' '.join(sys.argv), 'log_cron_gdrive.log')
                flag = True
            else:
                self.stdout.write('    \033[92mSUCCESS\033[0m: \033[94mconfig\033[0m settings uploaded.')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t))


        t = time.time()
        self.stdout.write('#5: Removing obsolete backups...')
        try:
            old = (datetime.date.today() - datetime.timedelta(days=KEEP_BACKUP)).strftime('%Y-%m-%dT00:00:00')
            list_mysql = subprocess.Popen(
                '%s && drive list -q "title contains \'%s_\' and (title contains \'_mysql.tgz\' or title contains \'_mysql_DEBUG.tgz\') and modifiedDate <= \'%s\'"| awk \'{printf $1" "}\'' % (gdrive_dir, env('SERVER_NAME'), old),
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            ).communicate()[0].strip().split()[1:]
            list_static = subprocess.Popen(
                '%s && drive list -q "title contains \'%s_\' and (title contains \'_static.tgz\' or title contains \'_static_DEBUG.tgz\') and modifiedDate <= \'%s\'"| awk \'{ printf $1" "}\'' % (gdrive_dir, env('SERVER_NAME'), old),
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            ).communicate()[0].strip().split()[1:]
            list_apache = subprocess.Popen(
                '%s && drive list -q "title contains \'%s_\' and (title contains \'_apache.tgz\' or title contains \'_apache_DEBUG.tgz\') and modifiedDate <= \'%s\'"| awk \'{ printf $1" "}\'' % (gdrive_dir, env('SERVER_NAME'), old),
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            ).communicate()[0].strip().split()[1:]
            list_config = subprocess.Popen(
                '%s && drive list -q "title contains \'%s_\' and (title contains \'_config.tgz\' or title contains \'_config_DEBUG.tgz\') and modifiedDate <= \'%s\'"| awk \'{ printf $1" "}\'' % (gdrive_dir, env('SERVER_NAME'), old),
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            ).communicate()[0].strip().split()[1:]
            list_all = list_mysql + list_static + list_apache + list_config
        except Exception:
            send_error_slack(traceback.format_exc(), 'Check Obsolete Backup Files', ' '.join(sys.argv), 'log_cron_gdrive.log')
            flag = True

        for id in list_all:
            try:
                subprocess.check_call(
                    '%s && drive info -i %s' % (gdrive_dir, id),
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                subprocess.check_call(
                    '%s && drive delete -i %s' % (gdrive_dir, id),
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
            except subprocess.CalledProcessError:
                send_error_slack(traceback.format_exc(), 'Remove Obsolete Backup Files', ' '.join(sys.argv), 'log_cron_gdrive.log')
                flag = True

        if not flag:
            self.stdout.write('    \033[92mSUCCESS\033[0m: \033[94m%s\033[0m obsolete backup files removed.' % len(list_all))
        self.stdout.write('Time elapsed: %.1f s.\n' % (time.time() - t))


        if flag:
            self.stdout.write('Finished with errors!')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t0))
            sys.exit(1)
        else:
            if DEBUG:
                self.stdout.write('\033[94m Uploaded to Google Drive. \033[0m')
            else:
                (t_cron, d_cron, t_now) = get_date_time('gdrive')
                gdrive_list = subprocess.Popen(
                    '%s && drive list -q "title contains \'%s_\' and title contains \'.tgz\'"' % (gdrive_dir, env('SERVER_NAME')),
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                ).communicate()[0].strip().split()[4:]
                html = 'File\t\t\t\tTime\t\t\t\tSize\n\n'
                for i in xrange(0, len(gdrive_list), 6):
                    html += '%s\t\t%s %s\t\t%s %s\n' % (gdrive_list[i + 1], gdrive_list[i + 4], gdrive_list[i + 5], gdrive_list[i + 2], gdrive_list[i + 3])

                if IS_SLACK:
                    if (not DEBUG) and BOT['SLACK']['ADMIN']['MSG_GDRIVE']:
                        send_notify_slack(
                            SLACK['ADMIN_NAME'],
                            '',
                            [{
                                'fallback': 'SUCCESS',
                                'mrkdwn_in': ['text'],
                                'color': 'good',
                                'text': '*SUCCESS*: Scheduled weekly *Gdrive Sync* finished @ _%s_\n' % time.ctime(),
                            }]
                        )
                        # send_notify_slack(SLACK['ADMIN_NAME'], '>```%s```\n' % html, '')
                else:
                    send_notify_emails(
                        '{%s} SYSTEM: Weekly Sync Notice' % env('SERVER_NAME'),
                        'This is an automatic email notification for the success of scheduled weekly sync of the %s Website backup contents to Google Drive account.\n\nThe crontab job is scheduled at %s (UTC) on every %sday.\n\nThe last system backup was performed at %s (PDT).\n\n%s\n\n%s Website Admin\n' % (env('SERVER_NAME'), t_cron, d_cron, t_now, html, env('SERVER_NAME'))
                    )
            get_backup_stat()
            self.stdout.write('Admin Backup Statistics refreshed.')

            self.stdout.write('All done successfully!')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t0))

