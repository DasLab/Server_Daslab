import subprocess
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.console import send_notify_slack, send_error_slack


class Command(BaseCommand):
    help = 'Restores MySQL database, static files, Apache2 settings and config settings from local backup/ folder.'

    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))

        flag = False
        t = time.time()
        self.stdout.write("#1: Restoring MySQL database...")
        try:
            subprocess.check_call('gunzip < %s/backup/backup_mysql.gz | mysql -u %s -p%s %s' % (MEDIA_ROOT, env.db()['USER'], env.db()['PASSWORD'], env.db()['NAME']), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            send_error_slack(traceback.format_exc(), 'Restore MySQL Database', ' '.join(sys.argv), 'log_cron_restore.log')
            flag = True
        else:
            self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94mMySQL\033[0m database overwritten.")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t))


        t = time.time()
        self.stdout.write("#2: Restoring static files...")
        try:
            subprocess.check_call('rm -rf %s/backup/data' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('cd %s/backup && tar zvxf backup_static.tgz' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('rm -rf %s/data' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('mv %s/backup/data %s/' % (MEDIA_ROOT, MEDIA_ROOT), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('rm -rf %s/backup/data' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if (not DEBUG):
                subprocess.check_call('%s/util_chmod.sh' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            send_error_slack(traceback.format_exc(), 'Restore Static Files', ' '.join(sys.argv), 'log_cron_restore.log')
            flag = True
        else:
            self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94mstatic\033[0m files overwritten.")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t))


        t = time.time()
        self.stdout.write("#3: Restoring apache2 settings...")
        try:
            subprocess.check_call('rm -rf %s/backup/apache2' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('cd %s/backup && tar zvxf backup_apache.tgz' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('rm -rf /etc/apache2', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('mv %s/backup/apache2 /etc/apache2 ' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('rm -rf %s/backup/apache2' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if (not DEBUG):
                subprocess.check_call('apache2ctl restart', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            send_error_slack(traceback.format_exc(), 'Restore Apache2 Settings', ' '.join(sys.argv), 'log_cron_restore.log')
            flag = True
        else:
            self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94mapache2\033[0m settings overwritten.")
        self.stdout.write("Time elapsed: %.1f s.\n" % (time.time() - t))


        t = time.time()
        self.stdout.write("#4: Restoring config settings...")
        try:
            subprocess.check_call('rm -rf %s/backup/config' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('cd %s/backup && tar zvxf backup_config.tgz' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('rm -rf %s/config', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('mv %s/backup/config %s/config ' (% MEDIA_ROOT, MEDIA_ROOT), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('rm -rf %s/backup/config' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if (not DEBUG):
                subprocess.check_call('apache2ctl restart', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            send_error_slack(traceback.format_exc(), 'Restore Config Settings', ' '.join(sys.argv), 'log_cron_restore.log')
            flag = True
        else:
            self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94mconfig\033[0m settings overwritten.")
        self.stdout.write("Time elapsed: %.1f s.\n" % (time.time() - t))


        if flag:
            self.stdout.write("Finished with errors!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(1)
        else:
            self.stdout.write("All done successfully!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
