import os
import subprocess
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.console import send_notify_slack, send_error_slack


class Command(BaseCommand):
    help = 'Collects system version information and outputs to cache/stat_sys.txt. Existing file will be overwritten.'

    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))

        d = time.strftime('%Y%m%d') #datetime.datetime.now().strftime('%Y%m%d')
        t = time.time()
        self.stdout.write("Checking system versions...")

        try:
            cpu = subprocess.Popen("uptime | sed 's/.*: //g' | sed 's/,/ \//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver = subprocess.Popen('uname -r | sed %s' % "'s/[a-z\-]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += '%s.%s.%s\t' % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
            ver += subprocess.Popen('python -c "import django; print %s"' % "django.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show django-crontab', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver += subprocess.Popen('head -4 %s | tail -1 | sed %s' % (os.path.join(MEDIA_ROOT, 'data/temp.txt'), "'s/.*: //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show django-environ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver += subprocess.Popen('head -4 %s | tail -1 | sed %s' % (os.path.join(MEDIA_ROOT, 'data/temp.txt'),"'s/.*: //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            ver += subprocess.Popen('mysql --version | sed %s | sed %s' % ("'s/,.*//g'", "'s/.*Distrib //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen('apachectl -v | head -1 | sed %s | sed %s' % ("'s/.*\///g'", "'s/[a-zA-Z \(\)]//g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            if DEBUG:
                ver += 'N/A\t'
            else:
                ver += subprocess.Popen('apt-cache show libapache2-mod-wsgi | grep Version | head -1 | sed %s | sed %s' % ("'s/.*: //g'", "'s/-.*//g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            if DEBUG:
                ver += 'N/A\t'
            else:
                ver += subprocess.Popen('apt-cache show libapache2-webauth | grep Version | sed %s | sed %s' % ("'s/.*: //g'", "'s/-.*//g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen("openssl version | sed 's/.*OpenSSL //g' | sed 's/[a-z].*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            if DEBUG:
                ver += 'N/A\t'
            else:
                ver += subprocess.Popen('wallet -v | sed %s' % "'s/.*wallet //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            ver_jquery = open(os.path.join(MEDIA_ROOT, 'media/js/jquery.min.js'), 'r').readline()
            ver += ver_jquery[ver_jquery.find('v')+1: ver_jquery.find('|')].strip() + '\t'
            ver_bootstrap = open(os.path.join(MEDIA_ROOT, 'media/js/bootstrap.min.js'), 'r').readlines()
            ver_bootstrap = ver_bootstrap[1]
            ver += ver_bootstrap[ver_bootstrap.find('v')+1: ver_bootstrap.find('(')].strip() + '\t'
            ver += subprocess.Popen('python -c "import suit, adminplus; print %s"' % "suit.VERSION, '\t', adminplus.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += '0.0.1\t'

            ver_swfobj = open(os.path.join(MEDIA_ROOT, 'media/js/swfobject.min.js'), 'r').readline()
            ver += ver_swfobj[ver_swfobj.find('v')+1: ver_swfobj.find('<')].strip() + '\t'
            ver_fullcall = open(os.path.join(MEDIA_ROOT, 'media/js/fullcalendar.min.js'), 'r').readlines()
            ver_fullcall = ver_fullcall[1]
            ver += ver_fullcall[ver_fullcall.find('v')+1:].strip() + '\t'
            ver_moment = open(os.path.join(MEDIA_ROOT, 'media/js/moment.min.js'), 'r').readlines()
            ver_moment = ver_moment[1]
            ver += ver_moment[ver_moment.find(':')+2:].strip() + '\t'
            # f = open(os.path.join(MEDIA_ROOT, 'media/js/dropzone.min.js'), 'r')
            # ver_dropz = ''.join(f.readlines())
            # ver_dropz = ver_dropz[ver_dropz.find('.version="') + 10 : ver_dropz.find('.version="') + 18]
            # ver += ver_dropz[:ver_dropz.find('"')] + '\t'
            # f.close()
            ver += 'place_holder\t'


            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show icalendar', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver += subprocess.Popen('head -4 %s | tail -1 | sed %s' % (os.path.join(MEDIA_ROOT, 'data/temp.txt'),"'s/.*: //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += '1.8.2\t'

            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('ssh -V 2', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver += subprocess.Popen('sed %s %s | sed %s | sed %s | sed %s' % ("'s/^OpenSSH\_//g'", os.path.join(MEDIA_ROOT, 'data/temp.txt'), "'s/U.*//'", "'s/,.*//g'", "'s/[a-z]/./g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen("git --version | sed 's/.*version //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            # ver += subprocess.Popen('python -c "from gitinspector import gitinspector; print gitinspector.version.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen("nano --version | head -1 | sed 's/.*version //g' | sed 's/(.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            ver += subprocess.Popen("drive -v | sed 's/.*v//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            if DEBUG:
                ver += subprocess.Popen("pandoc --version | head -1 | sed 's/.*pandoc //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            else:
                ver += subprocess.Popen("dpkg -l pandoc | tail -1 | sed 's/[a-z ]//g' | sed 's/-.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen("curl --version | head -1 | sed 's/.*curl //g' | sed 's/ (.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            ver += subprocess.Popen('python -c "import boto; print %s"' % "boto.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show pygithub', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver += subprocess.Popen('head -4 %s | tail -1 | sed %s' % (os.path.join(MEDIA_ROOT, 'data/temp.txt'),"'s/.*: //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show slacker', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver += subprocess.Popen('head -4 %s | tail -1 | sed %s' % (os.path.join(MEDIA_ROOT, 'data/temp.txt'),"'s/.*: //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen('python -c "import virtualenv, pip, simplejson, dropbox, requests; print %s"' % "dropbox.__version__, '\t', requests.__version__, '\t', simplejson.__version__, '\t', virtualenv.__version__, '\t', pip.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            ver += subprocess.Popen("java -jar %s/../yuicompressor.jar -V" % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            disk_sp = subprocess.Popen('df -h | grep "/dev/"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].split()
            ver += '%s / %s' % (disk_sp[3][:-1] + ' G', disk_sp[2][:-1] + ' G') + '\t'
            if DEBUG:
                mem_str = subprocess.Popen('top -l 1 | head -n 10 | grep PhysMem', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
                mem_avail = mem_str[mem_str.find(',')+1:mem_str.find('unused')].strip()
                if 'M' in mem_avail: 
                    mem_avail = '%.1f G' % (int(mem_avail[:-1]) / 1024.)
                else:
                    mem_avail = mem_avail[:-1] + ' ' + mem_avail[-1]
                mem_used = mem_str[mem_str.find(':')+1:mem_str.find('used')].strip()
                if 'M' in mem_used: 
                    mem_used = '%.1f G' % (int(mem_used[:-1]) / 1024.)
                else:
                    mem_used = mem_used[:-1] + ' ' + mem_used[-1]
            else:
                mem_str = subprocess.Popen('free -h', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split('\n')
                mem_str = subprocess.Popen('free -h', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split('\n')
                mem_str = [x for x in mem_str[2].split(' ') if x]
                mem_avail = mem_str[-1]
                if mem_avail[-1] == 'G': 
                    mem_avail = str(float(mem_avail[:-1]) * 1024) + ' M'
                else:
                    mem_avail = mem_avail[:-1] + ' M'
                mem_used = mem_str[-2]
                if mem_used[-1] == 'G': 
                    mem_used = str(float(mem_used[:-1]) * 1024) + ' M'
                else:
                    mem_used = mem_used[:-1] + ' M'
            ver += '%s / %s' % (mem_avail, mem_used) + '\t'
            ver += subprocess.Popen('du -h --total %s | tail -1' % os.path.join(MEDIA_ROOT, 'backup/backup_*.*gz'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
            ver += cpu + '\t'

            ver += '%s\t%s\t%s\t' % (MEDIA_ROOT, MEDIA_ROOT + '/data', MEDIA_ROOT + '/media')

            gdrive_dir = 'echo'
            if not DEBUG: gdrive_dir = 'cd %s' % APACHE_ROOT
            prefix = ''
            if DEBUG: prefix = '_DEBUG'
            ver += subprocess.Popen("%s && drive quota | awk '{ printf $2 \" G\t\"}'" % gdrive_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]

            open(os.path.join(MEDIA_ROOT, 'cache/stat_sys.txt'), 'w').write(ver)
            subprocess.Popen('rm %s' % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
            send_error_slack(traceback.format_exc(), 'Update System Versions', ' '.join(sys.argv), 'log_cron_version.log')

            self.stdout.write("Finished with \033[41mERROR\033[0m!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(1)

        self.stdout.write("Time elapsed: %.1f s.\n" % (time.time() - t))
        self.stdout.write("\033[92mSUCCESS\033[0m: \033[94mVersions\033[0m recorded in cache/stat_sys.txt.")
        self.stdout.write("All done successfully!")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))

