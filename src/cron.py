from datetime import datetime
# import os
import smtplib
import subprocess
import time
import traceback

# from django.core.mail import send_mail
from slacker import Slacker

from src.settings import *
from src.console import get_backup_stat, send_notify_emails, send_notify_slack


def get_date_time(keyword):
    t_cron = [c[0] for c in CRONJOBS if c[1].find(keyword) != -1][0]
    d_cron = ['Sun', 'Mon', 'Tues', 'Wednes', 'Thurs', 'Fri', 'Satur'][int(t_cron.split(' ')[-1])]
    t_cron = datetime.strptime(' '.join(t_cron.split(' ')[0:2]),'%M %H').strftime('%I:%M%p')
    t_now = datetime.now().strftime('%b %d %Y (%a) @ %H:%M:%S')
    return(t_cron, d_cron, t_now)


def backup_weekly():
    try:
        subprocess.check_call('cd %s && python manage.py backup' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print "    \033[41mERROR\033[0m: Failed to run \033[94mbackup_weekly()\033[0m schedule."
        err = traceback.format_exc()
        ts = '%s\t\tbackup_weekly()\n' % time.ctime()
        open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
        open('%s/cache/log_cron_backup.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
        if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *backup_weekly()* @ _%s_\n>```%s```\n' % (time.ctime(), err)}])
        raise Exception('Error with running scheduled backup_weekly().')
    else:
        (t_cron, d_cron, t_now) = get_date_time('backup')
        if DEBUG:
            print "\033[94m Backed up locally. \033[0m"
        else:
            local_list = subprocess.Popen('ls -gh %s/backup/*.*gz' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()
            html = 'File\t\t\t\tTime\t\t\t\tSize\n\n'
            for i in range(0, len(local_list), 8):
                html += '%s\t\t%s %s, %s\t\t%s\n' % (local_list[i+7], local_list[i+4], local_list[i+5], local_list[i+6], local_list[i+3])

            if IS_SLACK: 
                send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'SUCCESS', "mrkdwn_in": ["text"], "color":"good", "text":'*SUCCESS*: Scheduled weekly *backup* finished @ _%s_\n' % time.ctime()}])
                send_notify_slack(SLACK['ADMIN_NAME'], '>```%s```\n' % html, '')
            else:
                send_notify_emails('[System] {daslab.stanford.edu} Weekly Backup Notice', 'This is an automatic email notification for the success of scheduled weekly backup of the DasLab Website database and static contents.\n\nThe crontab job is scheduled at %s (UTC) on every %sday.\n\nThe last system backup was performed at %s (PDT).\n\n%s\n\nDasLab Website Admin\n' % (t_cron, d_cron, t_now, html))
        get_backup_stat()


def gdrive_weekly():
    try:
        subprocess.check_call('cd %s && python manage.py gdrive' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print "    \033[41mERROR\033[0m: Failed to run \033[94mgdrive_weekly()\033[0m schedule."
        err = traceback.format_exc()
        ts = '%s\t\tgdrive_weekly()\n' % time.ctime()
        open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
        open('%s/cache/log_cron_gdrive.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
        if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *gdrive_weekly()* @ _%s_\n>```%s```\n' % (time.ctime(), err)}])
        raise Exception('Error with running scheduled gdrive_weekly().')
    else:
        (t_cron, d_cron, t_now) = get_date_time('gdrive')
        if DEBUG:
            print "\033[94m Uploaded to Google Drive. \033[0m"
        else:
            gdrive_dir = 'echo'
            if not DEBUG: gdrive_dir = 'cd %s' % APACHE_ROOT
            gdrive_list = subprocess.Popen("%s && drive list -q \"title contains 'DasLab_'\"" % gdrive_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[4:]
            html = 'File\t\t\t\tTime\t\t\t\tSize\n\n'
            for i in range(0, len(gdrive_list), 6):
                html += '%s\t\t%s %s\t\t%s %s\n' % (gdrive_list[i+1], gdrive_list[i+4], gdrive_list[i+5], gdrive_list[i+2], gdrive_list[i+3])

            if IS_SLACK: 
                send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'SUCCESS', "mrkdwn_in": ["text"], "color":"good", "text":'*SUCCESS*: Scheduled weekly *gdrive sync* finished @ _%s_\n' % time.ctime()}])
                send_notify_slack(SLACK['ADMIN_NAME'], '>```%s```\n' % html, '')
            else:
                send_notify_emails('[System] {daslab.stanford.edu} Weekly Sync Notice', 'This is an automatic email notification for the success of scheduled weekly sync of the DasLab Website backup contents to Google Drive account.\n\nThe crontab job is scheduled at %s (UTC) on every %sday.\n\nThe last system backup was performed at %s (PDT).\n\n%s\n\nDasLab Website Admin\n' % (t_cron, d_cron, t_now, html))
        get_backup_stat()


def sys_ver_weekly():
    try:
        subprocess.check_call('cd %s && python manage.py versions' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print "    \033[41mERROR\033[0m: Failed to run \033[94msys_ver_weekly()\033[0m schedule."
        err = traceback.format_exc()
        ts = '%s\t\tsys_ver_weekly()\n' % time.ctime()
        open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
        open('%s/cache/log_cron_version.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
        if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *sys_ver_weekly()* @ _%s_\n>```%s```\n' % (time.ctime(), err)}])
        raise Exception('Error with running scheduled sys_ver_weekly().')


# def cache_every15min():
#     try:
#         subprocess.check_call('cd %s && python util_system_cache.py' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     except subprocess.CalledProcessError:
#         print "    \033[41mERROR\033[0m: Failed to run \033[94mcache_every15min()\033[0m schedule."
#         print traceback.format_exc()
#         raise Exception('Error with running scheduled cache_every15min().')


  
