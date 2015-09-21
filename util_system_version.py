import os
import subprocess
import sys
import time

t0 = time.time()
print time.ctime()
sys.path.append(os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings") 

from src.settings import *

d = time.strftime('%Y%m%d') #datetime.datetime.now().strftime('%Y%m%d')
t = time.time()
print "Checking system versions..."

cpu = subprocess.Popen("uptime | sed 's/.*: //g' | sed 's/,/ \//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

ver = subprocess.Popen('uname -r | sed %s' % "'s/[a-z\-]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
ver += '%s.%s.%s\t' % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
ver += subprocess.Popen('python -c "import django; print %s"' % "django.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

f = open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w')
f.write(subprocess.Popen('pip show django-crontab', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
f.close()
ver += subprocess.Popen('head -4 %s | tail -1 | sed %s' % (os.path.join(MEDIA_ROOT, 'data/temp.txt'), "'s/.*: //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
f = open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w')
f.write(subprocess.Popen('pip show django-environ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
f.close()
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
ver += 'wallet:N/A\t'

f = open(os.path.join(MEDIA_ROOT, 'media/js/jquery.min.js'), 'r')
ver_jquery = f.readline()
ver += ver_jquery[ver_jquery.find('v')+1: ver_jquery.find('|')].strip() + '\t'
f.close()
f = open(os.path.join(MEDIA_ROOT, 'media/js/bootstrap.min.js'), 'r')
f.readline()
ver_bootstrap = f.readline()
ver += ver_bootstrap[ver_bootstrap.find('v')+1: ver_bootstrap.find('(')].strip() + '\t'
f.close()
ver += subprocess.Popen('python -c "import suit, adminplus; print %s"' % "suit.VERSION, '\t', adminplus.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
ver += '0.0.1\t'

f = open(os.path.join(MEDIA_ROOT, 'media/js/swfobject.min.js'), 'r')
ver_swfobj = f.readline()
ver += ver_swfobj[ver_swfobj.find('v')+1: ver_swfobj.find('<')].strip() + '\t'
f.close()
f = open(os.path.join(MEDIA_ROOT, 'media/js/fullcalendar.min.js'), 'r')
f.readline()
ver_fullcall = f.readline()
ver += ver_fullcall[ver_fullcall.find('v')+1:].strip() + '\t'
f.close()
f = open(os.path.join(MEDIA_ROOT, 'media/js/moment.min.js'), 'r')
f.readline()
ver_moment = f.readline()
ver += ver_moment[ver_moment.find(':')+2:].strip() + '\t'
f.close()
# f = open(os.path.join(MEDIA_ROOT, 'media/js/dropzone.min.js'), 'r')
# ver_dropz = ''.join(f.readlines())
# ver_dropz = ver_dropz[ver_dropz.find('.version="') + 10 : ver_dropz.find('.version="') + 18]
# ver += ver_dropz[:ver_dropz.find('"')] + '\t'
# f.close()
ver += 'place_holder\t'


f = open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w')
f.write(subprocess.Popen('pip show icalendar', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
f.close()
ver += subprocess.Popen('head -4 %s | tail -1 | sed %s' % (os.path.join(MEDIA_ROOT, 'data/temp.txt'),"'s/.*: //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
ver += '1.8.2\t'

f = open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w')
f.write(subprocess.Popen('ssh -V 2', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
f.close()
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
f = open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w')
f.write(subprocess.Popen('pip show pygithub', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
f.close()
ver += subprocess.Popen('head -4 %s | tail -1 | sed %s' % (os.path.join(MEDIA_ROOT, 'data/temp.txt'),"'s/.*: //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
f = open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w')
f.write(subprocess.Popen('pip show slacker', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
f.close()
ver += subprocess.Popen('head -4 %s | tail -1 | sed %s' % (os.path.join(MEDIA_ROOT, 'data/temp.txt'),"'s/.*: //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
ver += subprocess.Popen('python -c "import virtualenv, pip, simplejson, dropbox, requests; print %s"' % "dropbox.__version__, '\t', requests.__version__, '\t', simplejson.__version__, '\t', virtualenv.__version__, '\t', pip.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

disk_sp = subprocess.Popen('df -h | head -2 | tail -1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].split()
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
    mem_avail = [x for x in mem_str[2].split(' ') if x][-1][:-1] + ' M'
    mem_used = [x for x in mem_str[2].split(' ') if x][-2][:-1] + ' M'
ver += '%s / %s' % (mem_avail, mem_used) + '\t'
ver += subprocess.Popen('du -h --total %s | tail -1' % os.path.join(MEDIA_ROOT, 'backup/backup_*.*gz'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
ver += cpu + '\t'

ver += '%s\t%s\t%s\t' % (MEDIA_ROOT, MEDIA_ROOT + '/data', MEDIA_ROOT + '/media')

gdrive_dir = 'echo'
if not DEBUG: gdrive_dir = 'cd %s' % APACHE_ROOT
prefix = ''
if DEBUG: prefix = '_DEBUG'
ver += subprocess.Popen("%s && drive quota | awk '{ printf $2 \" G\t\"}'" % gdrive_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]

f = open(os.path.join(MEDIA_ROOT, 'data/stat_sys.txt'), 'w')
f.write(ver)
f.close()
subprocess.Popen('rm %s' % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

print "Time elapsed: %.1f s." % (time.time() - t)
print
print "\033[92mSUCCESS\033[0m: \033[94mVersions\033[0m recorded in data/stat_sys.txt."
print "All done successfully!"
print "Time elapsed: %.1f s." % (time.time() - t0)
sys.exit(0)

