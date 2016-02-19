import os
import subprocess
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.console import get_backup_stat, send_notify_slack, send_error_slack


class Command(BaseCommand):
    help = 'Collects system version information and outputs to cache/stat_sys.txt. Existing file will be overwritten.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('manual', nargs='+', type=int, help='Flag for if force to run, choose from (0, 1).')


    def handle(self, *args, **options):
        if options['manual']:
            flag = (options['manual'][0] == 1)
        else:
            flag = False

        if not (BOT['SLACK']['IS_VERSION'] or flag): return
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))

        d = time.strftime('%Y%m%d') #datetime.datetime.now().strftime('%Y%m%d')
        t = time.time()
        ver = {}
        self.stdout.write("Checking system versions...")

        try:
            cpu = subprocess.Popen("uptime | sed 's/.*: //g' | sed 's/,/ \//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver['linux'] = subprocess.Popen("uname -r | sed 's/[a-z\-]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['python'] = '%s.%s.%s' % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
            ver['django'] = subprocess.Popen('python -c "import django; print django.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show django-crontab', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver['django_crontab'] = subprocess.Popen("head -4 %s | tail -1 | sed 's/.*: //g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show django-environ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver['django_environ'] = subprocess.Popen("head -4 %s | tail -1 | sed 's/.*: //g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver['mysql'] = subprocess.Popen("mysql --version | sed 's/,.*//g' | sed 's/.*Distrib //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['apache'] = subprocess.Popen("apachectl -v | head -1 | sed 's/.*\///g' | sed 's/[a-zA-Z \(\)]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            if DEBUG:
                ver['mod_wsgi'] = 'N/A'
            else:
                ver['mod_wsgi'] = subprocess.Popen("apt-cache show libapache2-mod-wsgi | grep Version | head -1 | sed 's/.*: //g' | sed 's/-.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            if DEBUG:
                ver['mod_webauth'] = 'N/A'
            else:
                ver['mod_webauth'] = subprocess.Popen('apt-cache show libapache2-webauth | grep Version | sed %s | sed %s' % ("'s/.*: //g'", "'s/-.*//g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['openssl'] = subprocess.Popen("openssl version | sed 's/.*OpenSSL //g' | sed 's/[a-z].*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            if DEBUG:
                ver['wallet'] = 'N/A'
            else:
                ver['wallet'] = subprocess.Popen('wallet -v | sed %s' % "'s/.*wallet //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver_jquery = open(os.path.join(MEDIA_ROOT, 'media/js/jquery.min.js'), 'r').readline()
            ver['jquery'] = ver_jquery[ver_jquery.find('v')+1: ver_jquery.find('|')].strip()
            ver_bootstrap = open(os.path.join(MEDIA_ROOT, 'media/js/bootstrap.min.js'), 'r').readlines()
            ver_bootstrap = ver_bootstrap[1]
            ver['bootstrap'] = ver_bootstrap[ver_bootstrap.find('v')+1: ver_bootstrap.find('(')].strip()
            ver['django_suit'] = subprocess.Popen('python -c "import suit; print suit.VERSION"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['django_adminplus'] = subprocess.Popen('python -c "import adminplus; print adminplus.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            if DEBUG:
                ver['django_filemanager'] = '0.0.2'
            else:
                open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show django-filemanager', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
                ver['django_filemanager'] = subprocess.Popen("head -4 %s | tail -1 | sed 's/.*: //g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver_swfobj = open(os.path.join(MEDIA_ROOT, 'media/js/swfobject.min.js'), 'r').readline()
            ver['swfobj'] = ver_swfobj[ver_swfobj.find('v')+1: ver_swfobj.find('<')].strip()
            ver_fullcall = open(os.path.join(MEDIA_ROOT, 'media/js/fullcalendar.min.js'), 'r').readlines()
            ver_fullcall = ver_fullcall[1]
            ver['fullcal']= ver_fullcall[ver_fullcall.find('v')+1:].strip()
            ver_moment = open(os.path.join(MEDIA_ROOT, 'media/js/moment.min.js'), 'r').readlines()
            ver_moment = ver_moment[1]
            ver['moment']= ver_moment[ver_moment.find(':')+2:].strip()
            # f = open(os.path.join(MEDIA_ROOT, 'media/js/dropzone.min.js'), 'r')
            # ver_dropz = ''.join(f.readlines())
            # ver_dropz = ver_dropz[ver_dropz.find('.version="') + 10 : ver_dropz.find('.version="') + 18]
            # ver += ver_dropz[:ver_dropz.find('"')] + '\t'
            # f.close()

            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show icalendar', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver['icalendar']= subprocess.Popen('head -4 %s | tail -1 | sed %s' % (os.path.join(MEDIA_ROOT, 'data/temp.txt'),"'s/.*: //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['gviz_api'] = '1.8.2'

            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('ssh -V', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver['ssh'] = subprocess.Popen("sed 's/^OpenSSH\_//g' %s | sed 's/U.*//' | sed 's/,.*//g' | sed 's/[a-z]/./g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['git'] = subprocess.Popen("git --version | sed 's/.*version //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['nano'] = subprocess.Popen("nano --version | head -1 | sed 's/.*version //g' | sed 's/(.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver['gdrive'] = subprocess.Popen("drive -v | sed 's/.*v//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            if DEBUG:
                ver['pandoc'] = subprocess.Popen("pandoc --version | head -1 | sed 's/.*pandoc //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            else:
                ver['pandoc'] = subprocess.Popen("dpkg -l pandoc | tail -1 | sed 's/[a-z ]//g' | sed 's/-.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['curl'] = subprocess.Popen("curl --version | head -1 | sed 's/.*curl //g' | sed 's/ (.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver['boto'] = subprocess.Popen('python -c "import boto; print boto.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show pygithub', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver['pygithub'] = subprocess.Popen("head -4 %s | tail -1 | sed 's/.*: //g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show slacker', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver['slacker'] = subprocess.Popen('head -4 %s | tail -1 | sed %s' % (os.path.join(MEDIA_ROOT, 'data/temp.txt'),"'s/.*: //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['dropbox']= subprocess.Popen('python -c "import dropbox; print dropbox.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['requests']= subprocess.Popen('python -c "import requests; print requests.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['simplejson']= subprocess.Popen('python -c "import simplejson; print simplejson.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['virtualenv']= subprocess.Popen('python -c "import virtualenv; print virtualenv.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['pip']= subprocess.Popen('python -c "import pip; print pip.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver['yuicompressor'] = subprocess.Popen("java -jar %s/../yuicompressor.jar -V" % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            disk_sp = subprocess.Popen('df -h | grep "/dev/"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].split()
            ver['_disk'] = [disk_sp[3][:-1] + ' G', disk_sp[2][:-1] + ' G']
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
            ver['_mem'] = [mem_avail, mem_used]
            ver['_cpu']= cpu.replace(' ', '').split('/')

            ver['_path'] = {
                'root' : MEDIA_ROOT,
                'data': MEDIA_ROOT + '/data',
                'media': MEDIA_ROOT + '/media'
            }

            gdrive_dir = 'echo'
            if not DEBUG: gdrive_dir = 'cd %s' % APACHE_ROOT
            prefix = ''
            if DEBUG: prefix = '_DEBUG'
            ver['_drive'] = subprocess.Popen("%s && drive quota | awk '{ printf $2 \" G\t\"}'" % gdrive_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split('\t')

            if not DEBUG:
                ver['ubuntu'] = subprocess.Popen("lsb_release -a | head -3 | tail -1 | sed 's/.*Ubuntu //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
                ver['htop'] = subprocess.Popen("htop --version | head -1 | sed 's/.*htop //g' | sed 's/ \-.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
                open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('aws --version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
                ver['aws_cli'] = subprocess.Popen("sed 's/ Python.*//g' %s | sed 's/.*\///g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver['screen'] = subprocess.Popen("screen --version | sed 's/.*version//g' | sed 's/(.*//g' | sed 's/[a-z ]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['bash'] = subprocess.Popen("bash --version | head -1 | sed 's/.*version//g' | sed 's/-release.*//g' | sed 's/[ ()]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['gcc'] = subprocess.Popen("gcc --version | head -1 | sed 's/.*) //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['make'] = subprocess.Popen("make --version | head -1 | sed 's/.*Make//g' | sed 's/ //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['cmake'] = subprocess.Popen("cmake --version | head -1 | sed 's/.*version//g' | sed 's/ //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['ninja'] = subprocess.Popen("ninja --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('javac -version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver['java'] = subprocess.Popen("sed 's/.*javac//g' %s | sed 's/_/./g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('perl -version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver['perl'] = subprocess.Popen("head -2 %s | tail -1 | sed 's/).*//g' | sed 's/.*(//g' | sed 's/[a-z]//g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['php'] = subprocess.Popen("php --version | head -1 | sed 's/\-.*//g' | sed 's/[A-Z ]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['ruby'] = subprocess.Popen("ruby --version | sed 's/.*ruby //g' | sed 's/ (.*//g' | sed 's/[a-z]/./g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['go'] = subprocess.Popen("go version | sed 's/.*version go//g' | sed 's/ .*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['coreutils'] = subprocess.Popen("tty --version | head -1 | sed 's/.*) //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['wget'] = subprocess.Popen("wget --version | head -1 | sed 's/.*Wget//g' | sed 's/built.*//g' | sed 's/ //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['tar'] = subprocess.Popen("tar --version | head -1 | sed 's/.*)//g' | sed 's/-.*//g' | sed 's/ //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['setuptools'] = subprocess.Popen('python -c "import setuptools; print setuptools.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['tkinter'] = subprocess.Popen('python -c "import Tkinter; print Tkinter.Tcl().eval(\'info patchlevel\')"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['imagemagick'] = subprocess.Popen("mogrify -version | head -1 | sed 's/\-.*//g' | sed 's/.*ImageMagick //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['kerberos'] = subprocess.Popen("klist -V | sed 's/.*version //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()


            open(os.path.join(MEDIA_ROOT, 'cache/stat_sys.json'), 'w').write(simplejson.dumps(ver, indent=' ' * 4, sort_keys=True))
            subprocess.Popen('rm %s' % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            get_backup_stat()


            if not DEBUG:
                ver_txt = "$(tput setab 1) ubuntu %s | linux %s | screen %s | bash %s | ssh %s $(tput sgr 0)\n$(tput setab 172) gcc %s | make %s | cmake %s | ninja %s |$(tput sgr 0)$(tput setab 15)$(tput setaf 16) mysql %s | django %s $(tput sgr 0)\n$(tput setab 11)$(tput setaf 16) python %s | java %s | perl %s | php %s | ruby %s | go %s $(tput sgr 0)\n$(tput setab 2) coreutils %s | wget %s | tar %s | curl %s | gdrive %s | pandoc %s $(tput sgr 0)\n$(tput setab 22) tkinter %s | virtualenv %s | setuptools %s | requests %s | simplejson %s $(tput sgr 0)\n$(tput setab 39) jquery %s | bootstrap %s | swfobject %s | moment %s | fullcalendar %s $(tput sgr 0)\n$(tput setab 20) crontab %s | environ %s | suit %s | adminplus %s | filemanager %s $(tput sgr 0)\n$(tput setab 55) boto %s | pygithub %s | slacker %s | dropbox %s | icalendar %s | gviz %s $(tput sgr 0)\n$(tput setab 171) apache %s | wsgi %s | webauth %s | openssl %s | wallet %s | kerberos %s $(tput sgr 0)\n$(tput setab 8) git %s | pip %s | nano %s | imagemagick %s | htop %s | awscli %s $(tput sgr 0)\n\n\n$(tput setab 15)$(tput setaf 16) Das Lab Website Server $(tput sgr 0)\n$(tput setab 15)$(tput setaf 16) daslab.stanford.edu / $(tput setaf 1)52$(tput setaf 16).$(tput setaf 2)25$(tput setaf 16).$(tput setaf 172)214$(tput setaf 16).$(tput setaf 4)40 $(tput sgr 0)\n" % (ver['ubuntu'], ver['linux'], ver['screen'], ver['bash'], ver['ssh'], ver['gcc'], ver['make'], ver['cmake'], ver['ninja'], ver['mysql'], ver['django'], ver['python'], ver['java'], ver['perl'], ver['php'], ver['ruby'], ver['go'], ver['coreutils'], ver['wget'], ver['tar'], ver['curl'], ver['gdrive'], ver['pandoc'], ver['tkinter'], ver['virtualenv'], ver['setuptools'], ver['requests'], ver['simplejson'], ver['jquery'], ver['bootstrap'], ver['swfobj'], ver['moment'], ver['fullcal'], ver['django_crontab'], ver['django_environ'], ver['django_suit'], ver['django_adminplus'], ver['django_filemanager'], ver['boto'], ver['pygithub'], ver['slacker'], ver['dropbox'], ver['icalendar'], ver['gviz_api'], ver['apache'], ver['mod_wsgi'], ver['mod_webauth'], ver['openssl'], ver['wallet'], ver['kerberos'], ver['git'], ver['pip'], ver['nano'], ver['imagemagick'], ver['htop'], ver['aws_cli'])
                subprocess.check_call('echo "%s" > %s/cache/sys_ver.txt' % (ver_txt, MEDIA_ROOT), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        except:
            send_error_slack(traceback.format_exc(), 'Update System Versions', ' '.join(sys.argv), 'log_cron_version.log')

            self.stdout.write("Finished with \033[41mERROR\033[0m!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(1)

        if (not DEBUG) and BOT['SLACK']['ADMIN']['MSG_VERSION']:
            send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'SUCCESS', "mrkdwn_in": ["text"], "color":"good", "text":'*SUCCESS*: Scheduled weekly *Version* finished @ _%s_\n' % time.ctime()}])
        self.stdout.write("Time elapsed: %.1f s.\n" % (time.time() - t))
        self.stdout.write("\033[92mSUCCESS\033[0m: \033[94mVersions\033[0m recorded in cache/stat_sys.txt.")
        self.stdout.write("All done successfully!")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))

