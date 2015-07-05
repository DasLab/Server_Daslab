import os
import simplejson
import subprocess
import sys

from django.core.management import call_command

from src.settings import MEDIA_ROOT, DEBUG
from src.models import BackupForm

def get_sys_stat():
    cpu = subprocess.Popen("uptime | sed 's/.*: //g' | sed 's/,/ \//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

    ver = subprocess.Popen('uname -r | sed %s' % "'s/[a-z\-]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += '%s.%s.%s\t' % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    ver += subprocess.Popen('python -c "import django, suit, adminplus; print %s"' % "django.__version__, '\t', suit.VERSION, '\t', adminplus.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

    f = open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w')
    f.write(subprocess.Popen('pip show django-crontab', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
    f.close()
    ver += subprocess.Popen('head -4 %s | tail -1 | sed %s' % (os.path.join(MEDIA_ROOT, 'data/temp.txt'), "'s/.*: //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    f = open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w')
    f.write(subprocess.Popen('pip show django-environ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
    f.close()
    ver += subprocess.Popen('head -4 %s | tail -1 | sed %s' % (os.path.join(MEDIA_ROOT, 'data/temp.txt'),"'s/.*: //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += '0.0.1\t'

    ver += subprocess.Popen('ls %s' % os.path.join(MEDIA_ROOT, 'media/js/jquery-*.min.js'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].replace(os.path.join(MEDIA_ROOT, 'media/js/jquery-'), '').replace('.min.js', '').strip() + '\t'
    f = open(os.path.join(MEDIA_ROOT, 'media/js/bootstrap.min.js'))
    f.readline()
    ver_bootstrap = f.readline()
    ver += ver_bootstrap[ver_bootstrap.find('v')+1: ver_bootstrap.find('(')].strip() + '\t'
    f.close()

    ver += subprocess.Popen('mysql --version | sed %s | sed %s' % ("'s/,.*//g'", "'s/.*Distrib //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen('apachectl -v | head -1 | sed %s | sed %s' % ("'s/.*\///g'", "'s/[a-zA-Z \(\)]//g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += 'N/A\t'

    f = open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w')
    f.write(subprocess.Popen('ssh -V 2', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
    f.close()
    ver += subprocess.Popen('sed %s %s | sed %s | sed %s | sed %s' % ("'s/^OpenSSH\_//g'", os.path.join(MEDIA_ROOT, 'data/temp.txt'), "'s/U.*//'", "'s/,.*//g'", "'s/[a-z]/./g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen("git --version | sed 's/.*version //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen("drive -v | sed 's/.*v//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

    ver += subprocess.Popen('python -c "import virtualenv, pip; print %s"' % "pip.__version__, '\t', virtualenv.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    
    disk_sp = subprocess.Popen('df -h | head -2 | tail -1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].split()
    ver += '%s / %s' % (disk_sp[3], disk_sp[2]) + '\t'
    if subprocess.Popen('uname', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() == 'Darwin':
        mem_str = subprocess.Popen('top -l 1 | head -n 10 | grep PhysMem', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
        mem_avail = mem_str[mem_str.find(',')+1:mem_str.find('unused')].strip()
        mem_used = mem_str[mem_str.find(':')+1:mem_str.find('used')].strip()
    else:
        mem_str = subprocess.Popen('free -h', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split('\n')
        mem_avail = [x for x in mem_str[2].split(' ') if x][-1]
        mem_used = [x for x in mem_str[2].split(' ') if x][-2]
    ver += '%s / %s' % (mem_avail, mem_used) + '\t'
    ver += subprocess.Popen('du -h --total %s | tail -1' % os.path.join(MEDIA_ROOT, 'backup/backup_*.*gz'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
    ver += cpu + '\t'

    ver += '%s\t%s\t%s\t' % (MEDIA_ROOT, MEDIA_ROOT + '/data', MEDIA_ROOT + '/media')

    f = open(os.path.join(MEDIA_ROOT, 'data/stat_sys.txt'), 'w')
    f.write(ver)
    f.close()
    subprocess.Popen('rm %s' % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def get_backup_stat():
    ver = str(int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/news_img/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1) + '\t'
    ver += subprocess.Popen('du -h %s' % os.path.join(MEDIA_ROOT, 'data/news_img/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
    ver += str(int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/ppl_img/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1) + '\t'
    ver += subprocess.Popen('du -h %s' % os.path.join(MEDIA_ROOT, 'data/ppl_img/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'

    ver += str(int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/pub_pdf/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1 + int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/pub_img/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1 + int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/pub_data/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1) + '\t'
    ver += subprocess.Popen('du -h --total %s %s %s | tail -1' % (os.path.join(MEDIA_ROOT, 'data/pub_pdf/'), os.path.join(MEDIA_ROOT, 'data/pub_img/'), os.path.join(MEDIA_ROOT, 'data/pub_data/')), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
    
    ver += str(int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/rot_ppt/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1 + int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/rot_data/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1) + '\t'
    ver += subprocess.Popen('du -h --total %s %s' % (os.path.join(MEDIA_ROOT, 'data/rot_ppt/'), os.path.join(MEDIA_ROOT, 'data/rot_data/')), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
    
    ver += str(int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/spe_ppt/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1) + '\t'
    ver += subprocess.Popen('du -h %s' % os.path.join(MEDIA_ROOT, 'data/spe_ppt/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'

    ver += subprocess.Popen('du -h %s' % os.path.join(MEDIA_ROOT, 'backup/backup_mysql.gz'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
    ver += subprocess.Popen('du -h %s' % os.path.join(MEDIA_ROOT, 'backup/backup_static.tgz'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
    ver += subprocess.Popen('du -h %s' % os.path.join(MEDIA_ROOT, 'backup/backup_apache.tgz'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
    ver += '%s\t%s\t%s\t' % (os.path.join(os.path.dirname(MEDIA_ROOT), 'backup/backup_mysql.gz'), os.path.join(os.path.dirname(MEDIA_ROOT), 'backup/backup_static.tgz'), os.path.join(os.path.dirname(MEDIA_ROOT), 'backup/backup_apache.tgz'))

    gdrive_dir = 'echo'
    if not DEBUG: gdrive_dir = 'cd /var/www'
    ver += '~|~'.join(subprocess.Popen("%s && drive list -q \"title contains 'DasLab_'\"" % gdrive_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[4:])

    f = open(os.path.join(MEDIA_ROOT, 'data/stat_backup.txt'), 'w')
    f.write(ver)
    f.close()
    subprocess.Popen('rm %s' % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def get_backup_form():
    cron = subprocess.Popen('crontab -l | cut -d" " -f1-5', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()
    day_backup = cron[4]
    day_upload = cron[9]
    time_backup = '%02d:%02d' % (int(cron[1]), int(cron[0]))
    time_upload = '%02d:%02d' % (int(cron[6]), int(cron[5]))

    json = {'day_backup':day_backup, 'day_upload':day_upload, 'time_backup':time_backup, 'time_upload':time_upload}
    return simplejson.dumps(json)


def set_backup_form(request):
    time_backup = request.POST['time_backup'].split(':')
    time_upload = request.POST['time_upload'].split(':')
    day_backup = request.POST['day_backup']
    day_upload = request.POST['day_upload']

    cron_backup = '%s %s * * %s' % (time_backup[1], time_backup[0], day_backup)
    cron_upload = '%s %s * * %s' % (time_upload[1], time_upload[0], day_upload)

    f = open('%s/cron.conf' % MEDIA_ROOT, 'r')
    lines = f.readlines()
    f.close()

    index =  [i for i, line in enumerate(lines) if 'src.cron.backup_weekly' in line or 'src.cron.gdrive_weekly' in line or 'KEEP_BACKUP' in line]
    lines[index[0]] = '\t\t["%s", "src.cron.backup_weekly"],\n' % cron_backup
    lines[index[1]] = '\t\t["%s", "src.cron.gdrive_weekly"]\n' % cron_upload
    lines[index[2]] = '\t"KEEP_BACKUP": %s\n' % request.POST['keep']

    f = open('%s/cron.conf' % MEDIA_ROOT, 'w')
    f.writelines(lines)
    f.close()
    # try:
    os.popen('crontab -r')
    os.popen('cd %s && python manage.py crontab add' % MEDIA_ROOT)
        # call_command('crontab', 'add')
        # call_command('crontab', 'add')
        # call_command('crontab', 'add')
        # call_command('crontab', 'add')
    # except:
        # pass


