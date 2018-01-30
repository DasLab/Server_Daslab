import os
import shutil
import subprocess
import sys
import tarfile
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.console import send_notify_slack, send_error_slack


class Command(BaseCommand):
    help = 'Restores MySQL database, static files, Apache2 settings and config settings from local backup/ folder.'

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
            self.stdout.write('#1: Restoring MySQL database...')
            try:
                tarfile.open('%s/backup/backup_mysql.tgz' % MEDIA_ROOT, 'r:gz').extractall()
                subprocess.check_call(
                    'cat %s/backup/backup_mysql | mysql -u %s -p%s %s' % (MEDIA_ROOT, env.db()['USER'], env.db()['PASSWORD'], env.db()['NAME']),
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                os.remove('%s/backup/backup_mysql' % MEDIA_ROOT)
            except Exception:
                send_error_slack(traceback.format_exc(), 'Restore MySQL Database', ' '.join(sys.argv), 'log_cron_restore.log')
                flag = True
            else:
                self.stdout.write('    \033[92mSUCCESS\033[0m: \033[94mMySQL\033[0m database overwritten.')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t))


        if is_static:
            t = time.time()
            self.stdout.write('#2: Restoring static files...')
            try:
                shutil.rmtree('%s/backup/data' % MEDIA_ROOT)
                tarfile.open('%s/backup/backup_static.tgz' % MEDIA_ROOT, 'r:gz').extractall()
                shutil.rmtree('%s/data' % MEDIA_ROOT)
                shutil.move('%s/backup/data' % MEDIA_ROOT, '%s' % MEDIA_ROOT)
                shutil.rmtree('%s/backup/data' % MEDIA_ROOT)
                if (not DEBUG):
                    subprocess.check_call(
                        '%s/util_chmod.sh' % MEDIA_ROOT,
                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                    )
            except Exception:
                send_error_slack(traceback.format_exc(), 'Restore Static Files', ' '.join(sys.argv), 'log_cron_restore.log')
                flag = True
            else:
                self.stdout.write('    \033[92mSUCCESS\033[0m: \033[94mstatic\033[0m files overwritten.')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t))


        if is_apache:
            t = time.time()
            self.stdout.write('#3: Restoring apache2 settings...')
            try:
                shutil.rmtree('%s/backup/apache2' % MEDIA_ROOT)
                tarfile.open('%s/backup/backup_apache.tgz' % MEDIA_ROOT, 'r:gz').extractall()
                shutil.rmtree('/etc/apache2')
                shutil.move('%s/backup/apache2' % MEDIA_ROOT, '/etc/apache2')
                shutil.rmtree('%s/backup/apache2' % MEDIA_ROOT)

                if (not DEBUG):
                    subprocess.check_call(
                        'apache2ctl restart',
                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                    )
            except Exception:
                send_error_slack(traceback.format_exc(), 'Restore Apache2 Settings', ' '.join(sys.argv), 'log_cron_restore.log')
                flag = True
            else:
                self.stdout.write('    \033[92mSUCCESS\033[0m: \033[94mapache2\033[0m settings overwritten.')
            self.stdout.write('Time elapsed: %.1f s.\n' % (time.time() - t))


        if is_config:
            t = time.time()
            self.stdout.write('#4: Restoring config settings...')
            try:
                shutil.rmtree('%s/backup/config' % MEDIA_ROOT)
                tarfile.open('%s/backup/backup_config.tgz' % MEDIA_ROOT, 'r:gz').extractall()
                shutil.rmtree('%s/config' % MEDIA_ROOT)
                shutil.move('%s/backup/config' % MEDIA_ROOT, '%s/config' % MEDIA_ROOT)
                shutil.rmtree('%s/backup/config' % MEDIA_ROOT)
                if (not DEBUG):
                    subprocess.check_call(
                        'apache2ctl restart',
                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                    )
            except Exception:
                send_error_slack(traceback.format_exc(), 'Restore Config Settings', ' '.join(sys.argv), 'log_cron_restore.log')
                flag = True
            else:
                self.stdout.write('    \033[92mSUCCESS\033[0m: \033[94mconfig\033[0m settings overwritten.')
            self.stdout.write('Time elapsed: %.1f s.\n' % (time.time() - t))


        if flag:
            self.stdout.write('Finished with errors!')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t0))
            sys.exit(1)
        else:
            self.stdout.write('All done successfully!')
            self.stdout.write('Time elapsed: %.1f s.' % (time.time() - t0))
