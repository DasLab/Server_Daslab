from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import glob
import operator
import os
import pickle
import pytz
import requests
import simplejson
import smtplib
import subprocess
import sys
import textwrap
import time
import traceback
import urllib

from icalendar import Calendar
import boto.ec2.cloudwatch, boto.ec2.elb
import gviz_api
from github import Github
import requests
from slacker import Slacker

from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings

from src.env import error400, error500
from src.settings import *
from src.models import BackupForm, ExportForm, BotSettingForm, Publication, SlackMessage

suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def send_notify_slack(msg_channel, msg_content, msg_attachment):
    if not settings._wrapped.IS_SLACK: return
    sh = Slacker(SLACK["ACCESS_TOKEN"])
    if msg_channel not in ['@', '@nobody']:
        sh.chat.post_message(msg_channel, msg_content, attachments=msg_attachment, as_user=False, parse='none', username='DasLab Bot', icon_url='https://daslab.stanford.edu/site_media/images/group/logo_bot.jpg')
    else:
        msg_channel = '[undesignated admin]'

    msg = SlackMessage(date=datetime.now(), receiver=msg_channel, content=msg_content, attachment=msg_attachment)
    msg.save()


def send_notify_emails(msg_subject, msg_content):
    # send_mail(msg_subject, msg_content, EMAIL_HOST_USER, [EMAIL_NOTIFY])
    smtpserver = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    smtpserver.starttls()
    smtpserver.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    msg = 'Subject: %s\n\n%s' % (msg_subject, msg_content)
    smtpserver.sendmail(EMAIL_HOST_USER, EMAIL_NOTIFY, msg)
    smtpserver.quit()


def send_error_slack(err, task='', fn='', log_file=''):
    if DEBUG: return
    if task:
        print "    \033[41mERROR\033[0m: Failed on \033[94m%s\033[0m." % task
        task = 'Failed on %s.\n' % task
    ts = '%s\t\t%s\n' % (time.ctime(), fn)
    open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
    if log_file:
        open('%s/cache/%s' % (MEDIA_ROOT, log_file), 'a').write('%s\n%s\n' % (ts, err))
    send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback": 'ERROR', "mrkdwn_in": ["text"], "color": "danger", "text": '*`ERROR`*: %s*%s* @ _%s_\n>```%s```\n' % (task, fn, time.ctime(), err)}])


def find_slack_id(name):
    sh = Slacker(SLACK["ACCESS_TOKEN"])
    users = sh.users.list().body['members']
    (sunet_id, who_id) = ('none', '')
    for resp in users:
        if resp.has_key('is_bot') and resp['is_bot']: continue
        if resp['profile']['real_name'].lower().startswith(name.lower()):
            if sunet_id != 'none':
                sunet_id = 'ambiguous'
                break
            email = resp['profile']['email']
            sunet_id = email[:email.find('@')]
            who_id = resp['name']

    if sunet_id == 'none':
        print '\033[41mERROR\033[0m: member (\033[94m%s\033[0m) not found.' % name
    elif sunet_id == 'ambiguous':
        print '\033[41mERROR\033[0m: member (\033[94m%s\033[0m) is ambiguate (more than 1 match).' % name
        who_id = ''
    return (who_id, sunet_id)


def get_date_time(keyword):
    t_cron = [c[0] for c in CRONJOBS if ''.join(c[2]).find(keyword) != -1][0]
    d_cron = ['Sun', 'Mon', 'Tues', 'Wednes', 'Thurs', 'Fri', 'Satur'][int(t_cron.split(' ')[-1])]
    t_cron = datetime.strptime(' '.join(t_cron.split(' ')[0:2]), '%M %H').strftime('%I:%M%p')
    t_now = datetime.now().strftime('%b %d %Y (%a) @ %H:%M:%S')
    return (t_cron, d_cron, t_now)


def humansize(nbytes):
    if nbytes == 0: return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.1f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def get_folder_size(path):
    total = 0
    for f in glob.glob(path):
        if os.path.isfile(f):
            total += os.path.getsize(f)
        else:
            total += get_folder_size(f + '/*')
    return total


def get_folder_num(path):
    total = 0
    for f in glob.glob(path):
        if os.path.isfile(f):
            total += 1
        else:
            total += get_folder_num(f + '/*')
    return total


def get_backup_stat():
    ver = {
        'news': [get_folder_num('%s/data/news_img/*' % MEDIA_ROOT), humansize(get_folder_size('%s/data/news_img/*' % MEDIA_ROOT))],
        'ppl': [get_folder_num('%s/data/news_img/*' % MEDIA_ROOT), humansize(get_folder_size('%s/data/ppl_img/*' % MEDIA_ROOT))],
        'pub': [sum([get_folder_num('%s/data/pub_pdf/*' % MEDIA_ROOT), get_folder_num('%s/data/pub_img/*' % MEDIA_ROOT), get_folder_num('%s/data/pub_data/*' % MEDIA_ROOT)]), humansize(sum([get_folder_size('%s/data/pub_pdf/*' % MEDIA_ROOT), get_folder_size('%s/data/pub_img/*' % MEDIA_ROOT), get_folder_size('%s/data/pub_data/*' % MEDIA_ROOT)]))],
        'roton': [sum([get_folder_num('%s/data/rot_ppt/*' % MEDIA_ROOT), get_folder_num('%s/data/rot_data/*' % MEDIA_ROOT)]), humansize(sum([get_folder_size('%s/data/rot_ppt/*' % MEDIA_ROOT), get_folder_size('%s/data/rot_data/*' % MEDIA_ROOT)]))],
        'arxiv': [get_folder_num('%s/data/spe_ppt/*' % MEDIA_ROOT), humansize(get_folder_size('%s/data/spe_ppt/*' % MEDIA_ROOT))],
        'defpos': [get_folder_num('%s/data/def_img/*' % MEDIA_ROOT), humansize(get_folder_size('%s/data/def_img/*' % MEDIA_ROOT))],
        'backup': {
            'mysql': [os.path.join(MEDIA_ROOT, 'backup/backup_mysql.tgz'), humansize(os.path.getsize('%s/backup/backup_mysql.tgz' % MEDIA_ROOT))],
            'data': [os.path.join(MEDIA_ROOT, 'backup/backup_static.tgz'), humansize(os.path.getsize('%s/backup/backup_static.tgz' % MEDIA_ROOT))],
            'apache': [os.path.join(MEDIA_ROOT, 'backup/backup_apache.tgz'), humansize(os.path.getsize('%s/backup/backup_apache.tgz' % MEDIA_ROOT))],
            'config': [os.path.join(MEDIA_ROOT, 'backup/backup_config.tgz'), humansize(os.path.getsize('%s/backup/backup_config.tgz' % MEDIA_ROOT))],
            'all': humansize(get_folder_size('%s/backup/*.*gz' % MEDIA_ROOT)),
        },
        'gdrive': []
    }

    gdrive_dir = 'echo' if DEBUG else 'cd %s' % APACHE_ROOT
    gdrive = subprocess.Popen("%s && drive list -q \"title contains '%s_' and title contains '.tgz'\"" % (gdrive_dir, env('SERVER_NAME')), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[4:]
    for i in xrange(0, len(gdrive), 6):
        ver['gdrive'].append([gdrive[i + 1], '%s %s' % (gdrive[i + 2], gdrive[i + 3]), '%s %s' % (gdrive[i + 4], gdrive[i + 5])])

    simplejson.dump(ver, open(os.path.join(MEDIA_ROOT, 'cache/stat_backup.json'), 'w'), indent=' ' * 4, sort_keys=True)
    subprocess.Popen('rm %s' % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def refresh_settings():
    (_, _, _, _, _, _, _, _, _, CRONJOBS, _, KEEP_BACKUP, BOT, IS_SLACK) = reload_conf(DEBUG, MEDIA_ROOT)
    settings._wrapped.CRONJOBS = CRONJOBS
    settings._wrapped.KEEP_BACKUP = KEEP_BACKUP
    settings._wrapped.BOT = BOT
    settings._wrapped.IS_SLACK = IS_SLACK


def get_sys_crontab():
    cron = subprocess.Popen('crontab -l', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].split('\n')
    (set_backup, set_upload, set_cache_3, set_cache_15, set_cache_30, set_duty_month, set_duty_quarter) = (('', ''), ('', ''), '', '', '', '', '')
    for cron_job in cron:
        array = cron_job.split()
        if 'backup_weekly' in cron_job:
            set_backup = ('%s:%s' % (array[1], array[0]), array[4])
        elif 'gdrive_weekly' in cron_job:
            set_upload = ('%s:%s' % (array[1], array[0]), array[4])
        elif 'cache_03' in cron_job:
            set_cache_3 = array[0].replace('*/', '')
        elif 'cache_15' in cron_job:
            set_cache_15 = array[0].replace('*/', '')
        elif 'cache_30' in cron_job:
            set_cache_30 = array[0].replace('*/', '')
        elif 'duty_monthly' in cron_job:
            set_duty_month = array[4]
        elif 'duty_quarterly' in cron_job:
            set_duty_quarter = array[4]

    return (set_backup, set_upload, set_cache_3, set_cache_15, set_cache_30, set_duty_month, set_duty_quarter)


def set_sys_crontab():
    try:
        subprocess.Popen('crontab -r', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        call_command('crontab', 'add')
    except subprocess.CalledProcessError:
        send_error_slack(traceback.format_exc(), 'Reset Crontab', 'set_backup_form', 'log_cron_backup.log')


def get_backup_form():
    refresh_settings()
    (set_backup, set_upload, _, _, _, _, _) = get_sys_crontab()
    return {'day_backup': set_backup[1], 'day_upload': set_upload[1], 'time_backup': set_backup[0], 'time_upload': set_upload[0], 'keep': settings._wrapped.KEEP_BACKUP}


def set_backup_form(request):
    form = BackupForm(request.POST)
    if not form.is_valid(): return 1

    cron_backup = '%s * * %s' % (form.cleaned_data['time_backup'].strftime('%M %H'), form.cleaned_data['day_backup'])
    cron_upload = '%s * * %s' % (form.cleaned_data['time_upload'].strftime('%M %H'), form.cleaned_data['day_upload'])

    env_cron = simplejson.load(open('%s/config/cron.conf' % MEDIA_ROOT))
    for cron_job in env_cron['CRONJOBS']:
        if 'backup_weekly' in cron_job[-1]:
            cron_job[0] = cron_backup
        elif 'gdrive_weekly' in cron_job[-1]:
            cron_job[0] = cron_upload
        suffix = cron_job[-1]
        cron_job[-1] = '>> %s/cache/log_cron.log 2>&1 # %s' % (MEDIA_ROOT, suffix[suffix.rfind(' # ') + 3:])
    env_cron['KEEP_BACKUP'] = form.cleaned_data['keep']
    simplejson.dump(env_cron, open('%s/config/cron.conf' % MEDIA_ROOT, 'w'), sort_keys=True, indent=' ' * 4)
    refresh_settings()
    set_sys_crontab()
    return 0


def get_bot_form():
    refresh_settings()
    BOT = settings._wrapped.BOT
    (_, _, set_cache_3, set_cache_15, set_cache_30, set_duty_month, set_duty_quarter) = get_sys_crontab()
    tp = simplejson.load(open('%s/cache/schedule.json' % MEDIA_ROOT, 'r'))['weekday']

    return {'is_slack': settings._wrapped.IS_SLACK, 'is_cache': BOT['CACHE']['IS_CACHE'], 'is_duty_bday': BOT['SLACK']['MSG_BDAY'], 'is_duty_breakfast': BOT['SLACK']['DUTY']['MONTH']['MSG_BDAY'], 'is_duty_aws': BOT['SLACK']['DUTY']['MONTH']['MSG_AWS'], 'is_duty_breakfast': BOT['SLACK']['DUTY']['MONTH']['MSG_BREAKFAST'], 'is_duty_schedule': BOT['SLACK']['DUTY']['MONTH']['MSG_SCHEDULE'], 'is_duty_website': BOT['SLACK']['DUTY']['MONTH']['MSG_WEBSITE'], 'is_duty_trip': BOT['SLACK']['DUTY']['QUARTER']['MSG_TRIP'], 'is_duty_git': BOT['SLACK']['DUTY']['QUARTER']['MSG_GIT'], 'is_admin_backup': BOT['SLACK']['ADMIN']['MSG_BACKUP'], 'is_admin_gdrive': BOT['SLACK']['ADMIN']['MSG_GDRIVE'], 'is_admin_version': BOT['SLACK']['ADMIN']['MSG_VERSION'], 'is_admin_report': BOT['SLACK']['ADMIN']['MSG_REPORT'], 'is_admin_aws_warn': BOT['SLACK']['ADMIN']['MSG_AWS_WARN'], 'is_version': BOT['SLACK']['IS_VERSION'], 'is_report': BOT['SLACK']['IS_REPORT'], 'is_bday': BOT['SLACK']['MSG_BDAY'], 'is_flash_slide': BOT['SLACK']['IS_FLASH_SETUP'], 'is_user_jc_1': BOT['SLACK']['REMINDER']['JC']['REMINDER_1'], 'is_user_jc_2': BOT['SLACK']['REMINDER']['JC']['REMINDER_2'], 'is_admin_jc': BOT['SLACK']['REMINDER']['JC']['REMINDER_ADMIN'], 'is_user_es_1': BOT['SLACK']['REMINDER']['ES']['REMINDER_1'], 'is_user_es_2': BOT['SLACK']['REMINDER']['ES']['REMINDER_2'], 'is_admin_es': BOT['SLACK']['REMINDER']['ES']['REMINDER_ADMIN'], 'is_user_rot_1': BOT['SLACK']['REMINDER']['ROT']['REMINDER_1'], 'is_user_rot_2': BOT['SLACK']['REMINDER']['ROT']['REMINDER_2'], 'is_admin_rot': BOT['SLACK']['REMINDER']['ROT']['REMINDER_ADMIN'], 'is_duty_mic': BOT['SLACK']['DUTY']['ETERNA']['MSG_MIC'], 'is_duty_broadcast': BOT['SLACK']['DUTY']['ETERNA']['MSG_BROADCAST'], 'is_duty_webnews': BOT['SLACK']['DUTY']['ETERNA']['MSG_NEWS'], 'day_duty_month': set_duty_month, 'day_duty_quarter': set_duty_quarter, 'day_meeting': tp, 'day_reminder_1': BOT['SLACK']['REMINDER']['DAY_BEFORE_REMINDER_1'], 'day_reminder_2': BOT['SLACK']['REMINDER']['DAY_BEFORE_REMINDER_2'], 'cache_3': set_cache_3, 'cache_15': set_cache_15, 'cache_30': set_cache_30}


def set_bot_form(request):
    form = BotSettingForm(request.POST)
    if not form.is_valid(): return 1

    BOT = {"SLACK":  {"IS_SLACK": form.cleaned_data['is_slack'], "IS_FLASH_SETUP": form.cleaned_data['is_flash_slide'], "IS_VERSION": form.cleaned_data['is_version'], "IS_REPORT": form.cleaned_data['is_report'], "MSG_BDAY": form.cleaned_data['is_bday'], "DUTY":  {"MONTH":  {"MSG_BDAY": form.cleaned_data['is_duty_bday'], "MSG_BREAKFAST": form.cleaned_data['is_duty_breakfast'], "MSG_AWS": form.cleaned_data['is_duty_aws'], "MSG_SCHEDULE": form.cleaned_data['is_duty_schedule'], "MSG_WEBSITE": form.cleaned_data['is_duty_website'], "WEEK_DAY": form.cleaned_data['day_duty_month']}, "QUARTER":  {"MSG_TRIP": form.cleaned_data['is_duty_trip'], "MSG_GIT": form.cleaned_data['is_duty_git'], "WEEK_DAY": form.cleaned_data['day_duty_quarter']}, "ETERNA":  {"MSG_MIC": form.cleaned_data['is_duty_mic'], "MSG_BROADCAST": form.cleaned_data['is_duty_broadcast'], "MSG_NEWS": form.cleaned_data['is_duty_webnews']} }, "REMINDER":  {"DAY_BEFORE_REMINDER_1":  form.cleaned_data['day_reminder_1'], "DAY_BEFORE_REMINDER_2":  form.cleaned_data['day_reminder_2'], "JC":  {"REMINDER_1": form.cleaned_data['is_user_jc_1'], "REMINDER_2": form.cleaned_data['is_user_jc_2'], "REMINDER_ADMIN": form.cleaned_data['is_admin_jc']}, "ES":  {"REMINDER_1": form.cleaned_data['is_user_es_1'], "REMINDER_2": form.cleaned_data['is_user_es_2'], "REMINDER_ADMIN": form.cleaned_data['is_admin_es']}, "ROT":  {"REMINDER_1": form.cleaned_data['is_user_rot_1'], "REMINDER_2": form.cleaned_data['is_user_rot_2'], "REMINDER_ADMIN": form.cleaned_data['is_admin_rot']} }, "ADMIN":  {"MSG_BACKUP": form.cleaned_data['is_admin_backup'], "MSG_GDRIVE": form.cleaned_data['is_admin_gdrive'], "MSG_VERSION": form.cleaned_data['is_admin_version'], "MSG_REPORT": form.cleaned_data['is_admin_report'], "MSG_AWS_WARN": form.cleaned_data['is_admin_aws_warn']} }, "CACHE":  { "IS_CACHE": form.cleaned_data['is_cache'], "INTERVAL_3": form.cleaned_data['cache_3'], "INTERVAL_15": form.cleaned_data['cache_15'], "INTERVAL_30": form.cleaned_data['cache_30']} }

    env_cron = simplejson.load(open('%s/config/cron.conf' % MEDIA_ROOT))
    for cron_job in env_cron['CRONJOBS']:
        if 'cache_03' in cron_job[-1]:
            cron_job[0] = '*/%s * * * *' % form.cleaned_data['cache_3']
        elif 'cache_15' in cron_job[-1]:
            cron_job[0] = '*/%s * * * *' % form.cleaned_data['cache_15']
        elif 'cache_30' in cron_job[-1]:
            cron_job[0] = '*/%s * * * *' % form.cleaned_data['cache_30']
        elif 'duty_monthly' in cron_job[-1]:
            cron_job[0] = '20 15 * * %s' % form.cleaned_data['day_duty_month']
        elif 'duty_quarterly' in cron_job[-1]:
            cron_job[0] = '25 15 * 1,4,7,10 %s' % form.cleaned_data['day_duty_quarter']
        suffix = cron_job[-1]
        cron_job[-1] = '>> %s/cache/log_cron.log 2>&1 # %s' % (MEDIA_ROOT, suffix[suffix.rfind(' # ') + 3:])

    simplejson.dump(env_cron, open('%s/config/cron.conf' % MEDIA_ROOT, 'w'), sort_keys=True, indent=' ' * 4)
    simplejson.dump(BOT, open('%s/config/bot.conf' % MEDIA_ROOT, 'w'), sort_keys=True, indent=' ' * 4)
    refresh_settings()
    set_sys_crontab()
    return 0


def restyle_apache():
    response = requests.get('https://%s/server-status/' % env('SSL_HOST'), auth=requests.auth.HTTPBasicAuth(env('APACHE_USER'), env('APACHE_PASSWORD'))).text.split('\n')

    title = 'Apache Server Status for <code>%s</code> (via <kbd>%s</kbd> )' % (env('SSL_HOST'), response[4].replace(')</h1>', '')[-13:].replace('via ', ''))
    ver = response[6].replace('<dl><dt>Server Version: Apache/', '').replace('(Ubuntu) OpenSSL/', '').replace('WebAuth/', '').replace('mod_wsgi/', '').replace('Python/', '').replace('</dt>', '').split()
    mpm = response[7].replace('<dt>Server MPM: ', '').replace('</dt>', '')
    tz = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone("America/Los_Angeles")).tzname()
    time_build = datetime.strftime(datetime.strptime(response[8].replace('<dt>Server Built: ', ''), '%Y-%m-%dT%H:%M:%S'), '%Y-%m-%d (%A) %I:%M:%S %p') + ' (%s)' % tz
    time_current = datetime.strftime(datetime.strptime(response[10].replace('<dt>Current Time: ', '').replace('</dt>', ''), '%A, %d-%b-%Y %H:%M:%S %Z'), '%Y-%m-%d (%A) %I:%M:%S %p') + ' (%s)' % tz
    time_restart = datetime.strftime(datetime.strptime(response[11].replace('<dt>Restart Time: ', '').replace('</dt>', ''), '%A, %d-%b-%Y %H:%M:%S %Z'), '%Y-%m-%d (%A) %I:%M:%S %p') + ' (%s)' % tz
    time_up = response[14].replace('<dt>Server uptime:  ', '').replace('</dt>', '').replace('hours', '<i>h</i>').replace('hour', '<i>h</i>').replace('minutes', '<i>min</i>').replace('minute', '<i>min</i>').replace('seconds', '<i>s</i>').replace('second', '<i>s</i>')

    server_load = response[15].replace('<dt>Server load: ', '').replace('</dt>', '').replace(' ', ' / ')
    total = response[16].replace('<dt>Total accesses: ', '').replace(' - Total Traffic:', '').replace('</dt>', '').split()
    cpu = response[17].replace('<dt>CPU Usage: ', '').replace('CPU load</dt>', '').replace(' -', '').replace('%', '').replace('</dt>', '').split()
    cpu_usage = '%.2f / %.2f / %.2f / %.2f' % (float(cpu[0][1:]), float(cpu[1][1:]), float(cpu[2][2:]), float(cpu[3][2:]))
    cpu_load = '%1.4f' % float(cpu[4])
    traffic = response[18].replace('<dt>', '').replace('B/request</dt>', '').replace('requests/sec -', '').replace('B/second -', '').split()
    if traffic[-1] in ('k', 'M', 'G'):
        traffic = '%1.2f / %.1f / %s' % (float(traffic[0]), float(traffic[-2]), traffic[-1])
    else:
        traffic = '%1.2f / %.1f' % (float(traffic[0]), float(traffic[-1]))
    workers = response[19].replace('<dt>', '').replace('requests currently being processed, ', '').replace('idle workers</dt>', '').split()
    worker = '<p style="margin-bottom:0px;">' + '</p><p style="margin-bottom:0px;">'.join(textwrap.wrap(response[20].replace('</dl><pre>', '').replace('</pre>', ''), 30)).replace('.', '<span class="label label-primary">.</span>').replace('_', '<span class="label label-inverse">_</span>').replace('S', '<span class="label label-default">S</span>').replace('R', '<span class="label label-violet">R</span>').replace('W', '<span class="label label-info">W</span>').replace('K', '<span class="label label-success">K</span>').replace('D', '<span class="label label-warning">D</span>').replace('C', '<span class="label label-danger">C</span>').replace('L', '<span class="label label-orange">L</span>').replace('G', '<span class="label label-green">G</span>').replace('I', '<span class="label label-brown">I</span>') + '</p>'

    table = ''.join(response[38:len(response)-23]).replace('<td>.</td>', '<td><span class="label label-primary">.</span></td>').replace('<td>_</td>', '<td><span class="label label-inverse">_</span></td>').replace('<td><b>S</b></td>', '<td><span class="label label-default">S</span></td>').replace('<td><b>R</b></td>', '<td><span class="label label-violet">R</span></td>').replace('<td><b>W</b></td>', '<td><span class="label label-info">W</span></td>').replace('<td><b>K</b></td>', '<td><span class="label label-success">K</span></td>').replace('<td><b>D</b></td>', '<td><span class="label label-warning">D</span></td>').replace('<td><b>C</b></td>', '<td><span class="label label-danger">C</span></td>').replace('<td><b>L</b></td>', '<td><span class="label label-orange">L</span></td>').replace('<td><b>G</b></td>', '<td><span class="label label-green">G</span></td>').replace('<td><b>I</b></td>', '<td><span class="label label-brown">I</span></td>')
    ssl = response[len(response)-6].replace('<b>', '').replace('</b>', '').replace('cache type: ', '').replace(', shared memory: ', '<br>').replace(' bytes, current entries: ', '<br>').replace('subcaches: ', '').replace(', indexes per subcache: ', '<br>').replace('index usage: ', '').replace(', cache usage: ', '<br>').split('<br>')
    ssl_subcache = '%s of %s' % (ssl[6], ssl[3])
    ssl_index = '%s of %s' % (ssl[5], ssl[4])
    port = response[len(response)-3].replace('</address>', '')[-3:]

    json = {'title': title, 'ver_apache': ver[0], 'ver_wsgi': ver[3], 'ver_webauth': ver[2], 'ver_ssl': ver[1], 'mpm': mpm, 'time_build': time_build, 'time_current': time_current, 'time_restart': time_restart, 'time_up': time_up, 'server_load': server_load, 'total_access': total[0], 'total_traffic': '%s %s' % (total[1], total[2]), 'cpu_load': cpu_load, 'cpu_usage': cpu_usage, 'traffic': traffic, 'idle': workers[1], 'processing': workers[0], 'worker': worker, 'table': table, 'port': port, 'ssl_subcache': ssl_subcache, 'ssl_index': ssl_index, 'ssl_cache': ssl[0], 'ssl_mem':  ssl[1], 'ssl_entry': ssl[2]}
    return simplejson.dumps(json, sort_keys=True, indent=' ' * 4)


def aws_result(results, args, req_id=None):
    data = []
    data.extend(results[0])
    for i, d in enumerate(data):
        ts = d[u'Timestamp'].replace(tzinfo=pytz.utc).astimezone(pytz.timezone(TIME_ZONE))
        d.update({u'Timestamp': ts})
        if args['calc_rate'] and 'Sum' in args['cols']:
            d.update({args['metric'][0] + u'Rate': round(d[u'Sum'] / args['period'], 3)})
        for j, r in enumerate(results):
            if j == 0 and len(results) > 1 and args['calc_rate']:
                continue
            keys = r[i].keys()
            keys.remove(u'Timestamp')
            keys.remove(u'Unit')
            for k in keys:
                val = r[i][k]
                name = args['metric'][j] + k
                if args['calc_rate'] and k == u'Sum':
                    val = val / args['period']
                    name = args['metric'][j] + u'Rate'
                d[name] = round(val, 3)
                if k in d: del d[k]

    desp = {'Timestamp': ('datetime', 'Timestamp'), 'Unit': ('string', args['unit'])}
    stats = ['Timestamp']
    for i, me in enumerate(args['metric']):
        if len(args['cols']) == len(args['metric']) and len(args['cols']) > 1:
            col = args['cols'][i]
            if col == 'Sum' and args['calc_rate']: col = 'Rate'
            desp[me + col] = ('number', me + col)
            stats.append(me + col)
        else:
            for col in args['cols']:
                if col == 'Sum' and args['calc_rate']: col = 'Rate'
                desp[me + col] = ('number', me + col)
                stats.append(me + col)

    data = sorted(data, key=operator.itemgetter(u'Timestamp'))
    data_table = gviz_api.DataTable(desp)
    data_table.LoadData(data)

    if (req_id is None) or (not req_id): req_id = '__REQ_ID__'
    return data_table.ToJSonResponse(columns_order=stats, order_by='Timestamp', req_id=req_id)


def aws_call(conn, args, qs, req_id=None):
    results = []
    for i, me in enumerate(args['metric']):
        col = args['cols']
        if len(args['cols']) == len(args['metric']) and len(args['cols']) > 1: col = args['cols'][i]
        data = conn.get_metric_statistics(args['period'], args['start_time'], args['end_time'], me, args['namespace'], col, args['dims'], args['unit'])

        temp = []
        for d in data:
            temp.append(d[u'Timestamp'])
        period = range(0, int((args['end_time'] - args['start_time']).total_seconds()), args['period'])
        for t in (args['start_time'] + timedelta(seconds=n) for n in period):
            t = t.replace(second=0, microsecond=0)
            if (not t in temp):
                data.append({u'Timestamp': t, u'Unit': args['unit'], unicode(args['cols'][0]): 0})

        if qs in ['lat', 'latency']:
            for d in data:
                d[u'Maximum'] = round(d[u'Maximum'] * 1000, 3)
        if qs in ['disk', 'net', 'volbytes', 'network']:
            for d in data:
                d[u'Sum'] = round(d[u'Sum'] / 1024, 3)
        results.append(data)
    return aws_result(results, args, req_id)


def aws_stats(request):
    if 'qs' in request.GET and 'sp' in request.GET and 'tqx' in request.GET:
        qs = request.GET.get('qs')
        sp = request.GET.get('sp')
        req_id = request.GET.get('tqx').replace('reqId:', '')

        if qs == 'init':
            conn = boto.ec2.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=True)
            resv = conn.get_only_instances(instance_ids=AWS['EC2_INSTANCE_ID'])
            stat = resv[0].__dict__
            stat1 = {k: stat[k] for k in ('id', 'instance_type', 'private_dns_name', 'public_dns_name', 'vpc_id', 'subnet_id', 'image_id', 'architecture')}
            resv = conn.get_all_volumes(volume_ids=AWS['EBS_VOLUME_ID'])
            stat = resv[0].__dict__
            stat2 = {k: stat[k] for k in ('id', 'type', 'size', 'zone', 'snapshot_id', 'encrypted')}

            conn = boto.ec2.elb.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=True)
            resv = conn.get_all_load_balancers(load_balancer_names=AWS['ELB_NAME'])
            stat = resv[0].__dict__
            stat3 = {k: stat[k] for k in ('dns_name', 'vpc_id', 'subnets', 'health_check')}
            stat3['health_check'] = str(stat3['health_check']).replace('HealthCheck:', '')

            return simplejson.dumps({'ec2': stat1, 'ebs': stat2, 'elb': stat3}, sort_keys=True, indent=' ' * 4)

        else:
            conn = boto.ec2.cloudwatch.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=True)
            if sp == '7d':
                args = {'period': 10800, 'start_time': datetime.utcnow() - timedelta(days=7), 'end_time': datetime.utcnow()}
            elif sp == '48h':
                args = {'period': 720, 'start_time': datetime.utcnow() - timedelta(hours=48), 'end_time': datetime.utcnow()}
            else:
                return error400(request)

            if qs == 'latency':
                args.update({'metric': ['Latency'], 'namespace': 'AWS/ELB', 'cols': ['Maximum'], 'dims': {}, 'unit': 'Seconds', 'calc_rate': False})
            elif qs == 'request':
                args.update({'metric': ['RequestCount'], 'namespace': 'AWS/ELB', 'cols': ['Sum'], 'dims': {}, 'unit': 'Count', 'calc_rate': False})
            elif qs == '23xx':
                args.update({'metric': ['HTTPCode_Backend_2XX', 'HTTPCode_Backend_3XX'], 'namespace': 'AWS/ELB', 'cols': ['Sum'], 'dims': {}, 'unit': 'Count', 'calc_rate': False})
            elif qs == '45xx':
                args.update({'metric': ['HTTPCode_Backend_4XX', 'HTTPCode_Backend_5XX'], 'namespace': 'AWS/ELB', 'cols': ['Sum'], 'dims': {}, 'unit': 'Count', 'calc_rate': False})
            elif qs == 'host':
                args.update({'metric': ['HealthyHostCount', 'UnHealthyHostCount'], 'namespace': 'AWS/ELB', 'cols': ['Minimum', 'Maximum'], 'dims': {}, 'unit': 'Count', 'calc_rate': False})
            elif qs == 'status':
                args.update({'metric': ['BackendConnectionErrors', 'StatusCheckFailed_Instance', 'StatusCheckFailed_System'], 'namespace': 'AWS/EC2', 'cols': ['Sum'], 'dims': {}, 'unit': 'Count', 'calc_rate': False})
            elif qs == 'network':
                args.update({'metric': ['NetworkIn', 'NetworkOut'], 'namespace': 'AWS/EC2', 'cols': ['Sum'], 'dims': {}, 'unit': 'Bytes', 'calc_rate': True})
            elif qs == 'cpu':
                args.update({'metric': ['CPUUtilization'], 'namespace': 'AWS/EC2', 'cols': ['Average'], 'dims': {}, 'unit': 'Percent', 'calc_rate': False})
            elif qs == 'credit':
                args.update({'metric': ['CPUCreditUsage', 'CPUCreditBalance'], 'namespace': 'AWS/EC2', 'cols': ['Average'], 'dims': {}, 'unit': 'Count', 'calc_rate': False})
            elif qs == 'volops':
                args.update({'metric': ['VolumeWriteOps', 'VolumeReadOps'], 'namespace': 'AWS/EBS', 'cols': ['Sum'], 'dims': {}, 'unit': 'Count', 'calc_rate': False})
            elif qs == 'volbytes':
                args.update({'metric': ['VolumeWriteBytes', 'VolumeReadBytes'], 'namespace': 'AWS/EBS', 'cols': ['Sum'], 'dims': {}, 'unit': 'Bytes', 'calc_rate': True})
            else:
                return error400(request)
    else:
        return error400(request)

    if args['namespace'] == 'AWS/ELB':
        args['dims'] = {'LoadBalancerName': AWS['ELB_NAME']}
    elif args['namespace'] == 'AWS/EC2':
        args['dims'] = {'InstanceId': AWS['EC2_INSTANCE_ID']}
    elif args['namespace'] == 'AWS/EBS':
        args['dims'] = {'VolumeId': AWS['EBS_VOLUME_ID']}

    return aws_call(conn, args, qs, req_id)


def ga_stats(request):
    if 'qs' in request.GET and 'tqx' in request.GET:
        qs = request.GET.get('qs')
        req_id = request.GET.get('tqx').replace('reqId:', '')
        access_token = requests.post('https://www.googleapis.com/oauth2/v3/token?refresh_token=%s&client_id=%s&client_secret=%s&grant_type=refresh_token' % (GA['REFRESH_TOKEN'], GA['CLIENT_ID'], GA['CLIENT_SECRET'])).json()['access_token']
        stats = {}
        url_colon = urllib.quote(':')
        url_comma = urllib.quote(',')

        if qs == 'init':
            temp = requests.get('https://www.googleapis.com/analytics/v3/data/ga?ids=ga%s%s&start-date=30daysAgo&end-date=yesterday&metrics=ga%ssessionDuration%sga%sbounceRate%sga%spageviewsPerSession%sga%spageviews%sga%ssessions%sga%susers&access_token=%s' % (url_colon, GA['ID'], url_colon, url_comma, url_colon, url_comma, url_colon, url_comma, url_colon, url_comma, url_colon, url_comma, url_colon, access_token)).json()['totalsForAllResults']
            temp_prev = requests.get('https://www.googleapis.com/analytics/v3/data/ga?ids=ga%s%s&start-date=60daysAgo&end-date=30daysAgo&metrics=ga%ssessionDuration%sga%sbounceRate%sga%spageviewsPerSession%sga%spageviews%sga%ssessions%sga%susers&access_token=%s' % (url_colon, GA['ID'], url_colon, url_comma, url_colon, url_comma, url_colon, url_comma, url_colon, url_comma, url_colon, url_comma, url_colon, access_token)).json()['totalsForAllResults']

            for i, key in enumerate(temp):
                ga_key = key[3:]
                if ga_key in ['bounceRate', 'pageviewsPerSession']:
                    prev = '%.2f' % (float(temp[key]) - float(temp_prev[key]))
                    curr = '%.2f' % float(temp[key])
                elif ga_key == 'sessionDuration':
                    diff = int(float(temp[key]) / 1000) - int(float(temp_prev[key]) / 1000)
                    prev = str(timedelta(seconds=abs(diff)))
                    if diff < 0: prev = '-%s' % prev
                    curr = str(timedelta(seconds=int(float(temp[key]) / 1000)))
                else:
                    prev = '%d' % (int(temp[key]) - int(temp_prev[key]))
                    curr = '%d' % int(temp[key])
                stats.update({ga_key: curr, (ga_key + '_prev'): prev})
            return simplejson.dumps(stats, sort_keys=True, indent=' ' * 4)

        elif 'sp' in request.GET:
            sp = request.GET.get('sp')

            if qs == 'chart':
                (dm, strpt) = ('date', '%Y%m%d')
                if sp == '24h':
                    (d1, d2, dm, strpt, ts) = ('yesterday', 'today', 'dateHour', '%Y%m%d%H', 'datetime')
                elif sp == '7d':
                    (d1, d2, ts) = ('7daysAgo', 'today', 'date')
                elif sp == '1m':
                    (d1, d2, ts) = ('30daysAgo', 'yesterday', 'date')
                elif sp == '3m':
                    (d1, d2, ts) = ('90daysAgo', 'yesterday', 'date')
                else:
                    return error400(request)

                i = 0
                while True:
                    temp = requests.get('https://www.googleapis.com/analytics/v3/data/ga?ids=ga%s%s&start-date=%s&end-date=%s&metrics=ga%ssessions&dimensions=ga%s%s&access_token=%s' % (url_colon, GA['ID'], d1, d2, url_colon, url_colon, dm, access_token)).json()
                    if 'rows' in temp:
                        temp = temp['rows']
                        break
                    time.sleep(2)
                    i += 1
                    if i == 3: return error500(request)

                data = []
                stats = ['Timestamp', 'Sessions']
                desp = {'Timestamp': (ts, 'Timestamp'), 'Sessions': ('number', 'Sessions')}

                for row in temp:
                    ts = datetime.strptime(row[0], strpt)
                    ts = ts if sp == '24h' else ts.date()
                    data.append({u'Timestamp': ts, 'Sessions': float(row[1])})
                data = sorted(data, key=operator.itemgetter(stats[0]))
                data_table = gviz_api.DataTable(desp)
                data_table.LoadData(data)
                return data_table.ToJSonResponse(columns_order=stats, order_by='Timestamp', req_id=req_id)

            elif qs == 'pie':
                if sp == 'session':
                    (me, dm, field) = ('sessions', 'userType', 'Sessions')
                elif sp == 'user':
                    (me, dm, field) = ('users', 'userType', 'Visitors')
                elif sp == 'browser':
                    (me, dm, field) = ('users', 'browser', 'Browsers')
                elif sp == 'pageview':
                    (me, dm, field) = ('pageviews', 'userType', 'Page Views')
                else:
                    return error400(request)

                i = 0
                while True:
                    temp = requests.get('https://www.googleapis.com/analytics/v3/data/ga?ids=ga%s%s&start-date=30daysAgo&end-date=yesterday&metrics=ga%s%s&dimensions=ga%s%s&access_token=%s' % (url_colon, GA['ID'], url_colon, me, url_colon, dm, access_token)).json()
                    if 'rows' in temp:
                        temp = temp['rows']
                        break
                    time.sleep(2)
                    i += 1
                    if i == 3: return error500(request)

                data = []
                stats = ['Category', field]
                desp = {'Category': ('string', 'Category'), field: ('number', field)}

                for row in temp:
                    data.append({'Category': row[0], field: float(row[1])})
                data = sorted(data, key=operator.itemgetter(stats[0]))
                if sp == 'browser':
                    data = sorted(data, key=operator.itemgetter(stats[1]), reverse=True)[:min(len(data), 4)]
                data_table = gviz_api.DataTable(desp)
                data_table.LoadData(data)
                return data_table.ToJSonResponse(columns_order=stats, order_by='Timestamp', req_id=req_id)
            else:
                return error400(request)

        elif qs == 'geo':
            i = 0
            while True:
                temp = requests.get('https://www.googleapis.com/analytics/v3/data/ga?ids=ga%s%s&start-date=30daysAgo&end-date=yesterday&metrics=ga%ssessions&dimensions=ga%scountry&access_token=%s' % (url_colon, GA['ID'], url_colon, url_colon, access_token)).json()
                if 'rows' in temp:
                    temp = temp['rows']
                    break
                time.sleep(2)
                i += 1
                if i == 3: return error500(request)

            data = []
            stats = ['Country', 'Sessions']
            desp = {'Country': ('string', 'Country'), 'Sessions': ('number', 'Sessions')}

            for row in temp:
                data.append({'Country': row[0], 'Sessions': float(row[1])})
            data = sorted(data, key=operator.itemgetter(stats[0]))
            data_table = gviz_api.DataTable(desp)
            data_table.LoadData(data)
            return data_table.ToJSonResponse(columns_order=stats, order_by='Timestamp', req_id=req_id)

        else:
            return error400(request)
    else:
        return error400(request)


def git_stats(request):
    if 'qs' in request.GET and 'tqx' in request.GET:
        qs = request.GET.get('qs')
        req_id = request.GET.get('tqx').replace('reqId:', '')
        gh = Github(login_or_token=GIT["ACCESS_TOKEN"])
        repo_name = GIT["REPOSITORY"]
        repo = gh.get_repo(repo_name)

        if qs in ['init', 'num']:
            if qs == 'init':
                data = []
                i = 0
                contribs = repo.get_stats_contributors()
                while (contribs is None and i <= 5):
                    time.sleep(1)
                    contribs = repo.get_stats_contributors()
                    i += 1
                if contribs is None: return error500(request)

                for contrib in contribs:
                    a, d = (0, 0)
                    for w in contrib.weeks:
                        a += w.a
                        d += w.d
                    au = '(None)' if not contrib.author else '<i>%s</i> <span style="color:#888">(%s)</span>' % (contrib.author.login, contrib.author.name)
                    data.append({u'Contributors': au, u'Commits': contrib.total, u'Additions': a, u'Deletions': d})
                data = sorted(data, key=operator.itemgetter(u'Commits'))
                return simplejson.dumps({'contrib': data}, sort_keys=True, indent=' ' * 4)
            else:
                created_at = repo.created_at.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(TIME_ZONE)).strftime('%Y-%m-%d %H:%M:%S')
                pushed_at = repo.pushed_at.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(TIME_ZONE)).strftime('%Y-%m-%d %H:%M:%S')

                num_issues = len(requests.get('https://api.github.com/repos/' + repo_name + '/issues?access_token=%s' % GIT['ACCESS_TOKEN']).json())
                num_pulls = len(requests.get('https://api.github.com/repos/' + repo_name + '/pulls?access_token=%s' % GIT['ACCESS_TOKEN']).json())
                num_watchers = len(requests.get('https://api.github.com/repos/' + repo_name + '/watchers?access_token=%s' % GIT['ACCESS_TOKEN']).json())
                num_branches = len(requests.get('https://api.github.com/repos/' + repo_name + '/branches?access_token=%s' % GIT['ACCESS_TOKEN']).json())
                num_forks = len(requests.get('https://api.github.com/repos/' + repo_name + '/forks?access_token=%s' % GIT['ACCESS_TOKEN']).json())
                num_downloads = len(requests.get('https://api.github.com/repos/' + repo_name + '/downloads?access_token=%s' % GIT['ACCESS_TOKEN']).json())
                return simplejson.dumps({'created_at': created_at, 'pushed_at': pushed_at, 'num_watchers': num_watchers, 'num_pulls': num_pulls, 'num_issues': num_issues, 'num_branches': num_branches, 'num_forks': num_forks, 'num_downloads': num_downloads}, sort_keys=True, indent=' ' * 4)

        else:
            data = []
            desp = {'Timestamp': ('date', 'Timestamp')}
            stats = ['Timestamp']

            if qs == 'c':
                i = 0
                contribs = repo.get_stats_commit_activity()
                while (contribs is None and i <= 5):
                    time.sleep(1)
                    contribs = repo.get_stats_commit_activity()
                    i += 1
                if contribs is None: return error500(request)
                fields = ['Commits']
                for contrib in contribs:
                    for i, day in enumerate(contrib.days):
                        data.append({u'Timestamp': (contrib.week + timedelta(days=i)).date(), u'Commits': day})
            elif qs == 'ad':
                i = 0
                contribs = repo.get_stats_code_frequency()
                while (contribs is None and i <= 5):
                    time.sleep(1)
                    contribs = repo.get_stats_code_frequency()
                    i += 1
                if contribs is None: return error500(request)
                fields = ['Additions', 'Deletions']
                for contrib in contribs:
                    data.append({u'Timestamp': contrib.week.date(), u'Additions': contrib.additions, u'Deletions': contrib.deletions})
            elif qs == 'au':
                i = 0
                contribs = repo.get_stats_contributors()
                while (contribs is None and i <= 5):
                    time.sleep(1)
                    contribs = repo.get_stats_contributors()
                    i += 1
                if contribs is None: return error500(request)
                fields = ['Commits', 'Additions', 'Deletions']
                for contrib in contribs:
                    a, d = (0, 0)
                    for w in contrib.weeks:
                        a += w.a
                        d += w.d
                    au = contrib.author.login if contrib.author else '(None)'
                    data.append({u'Contributors': au, u'Commits': contrib.total, u'Additions': a, u'Deletions': d})
                stats = ['Contributors']
                desp['Contributors'] = ('string', 'Name')
                del desp['Timestamp']
            else:
                return error400(request)

            for field in fields:
                stats.append(field)
                desp[field] = ('number', field)

            data = sorted(data, key=operator.itemgetter(stats[0]))
            data_table = gviz_api.DataTable(desp)
            data_table.LoadData(data)
            results = data_table.ToJSonResponse(columns_order=stats, order_by='Timestamp', req_id=req_id)
            return results
    else:
        return error400(request)


def export_citation(request):
    form = ExportForm(request.POST)
    if not form.is_valid(): return render(request, PATH.HTML_PATH['admin_export'], {'form': ExportForm()})

    is_order_number = form.cleaned_data['order_number']
    is_quote_title = form.cleaned_data['quote_title']
    is_double_space = form.cleaned_data['double_space']
    is_include_preprint = form.cleaned_data['include_preprint']
    is_include_hidden = form.cleaned_data['include_hidden']

    text_type = form.cleaned_data['text_type']
    year_start = form.cleaned_data['year_start']
    number_order = form.cleaned_data['number_order'] == '1'
    sort_order = 'display_date'
    if form.cleaned_data['sort_order'] == '1': sort_order = '-' + sort_order

    publications = Publication.objects.filter(year__gte=year_start).order_by(sort_order)
    if not is_include_preprint: publications = publications.filter(is_preprint=False)
    if not is_include_hidden: publications = publications.filter(is_visible=True)

    if text_type == '0':
        txt = ''
        for i, pub in enumerate(publications):
            order = ''
            if is_order_number:
                if number_order:
                    order = '%d. ' % (len(publications) - i)
                else:
                    order = '%d. ' % (i + 1)

            title = pub.title
            if is_quote_title: title = '"%s"' % title
            number = pub.volume
            if pub.issue: number += '(%s)' % pub.issue
            page = ''
            if pub.begin_page: page += ': %s' % pub.begin_page
            if pub.end_page: page += '-%s' % pub.end_page
            double_space = ''
            if is_double_space: double_space = '\n'
            txt += '%s%s (%s) %s %s %s%s\n%s' % (order, pub.authors, pub.year, title, pub.journal, number, page, double_space)

        response = HttpResponse(txt, content_type='text/plain')
    else:
        is_bold_author = form.cleaned_data['bold_author']
        is_bold_year = form.cleaned_data['bold_year']
        is_underline_title = form.cleaned_data['underline_title']
        is_italic_journal = form.cleaned_data['italic_journal']
        is_bold_volume = form.cleaned_data['bold_volume']

        html = '<html><body>'
        for i, pub in enumerate(publications):
            order = ''
            if is_order_number:
                if number_order:
                    order = '%d. ' % (len(publications) - i)
                else:
                    order = '%d. ' % (i + 1)

            authors = pub.authors
            if is_bold_author: authors = authors.replace('Das, R.', '<b>Das, R.</b>').replace('Das R.', '<b>Das, R.</b>')
            year = pub.year
            if is_bold_year: year = '<b>%s</b>' % year
            title = pub.title
            if is_underline_title: title = '<u>%s</u>' % title
            if is_quote_title: title = '&quot;%s&quot;' % title
            journal = pub.journal
            if is_italic_journal: journal = '<i>%s</i>' % journal
            number = pub.volume
            if is_bold_volume: number = '<b>%s</b>' % number
            if pub.issue: number += '(%s)' % pub.issue
            page = ''
            if pub.begin_page: page += ': %s' % pub.begin_page
            if pub.end_page: page += '-%s' % pub.end_page
            double_space = ''
            if is_double_space: double_space = '<br/>'
            html += '<p>%s%s (%s) %s %s %s%s</p>%s' % (order, authors, year, title, journal, number, page, double_space)

        html += '</body></html>'
        response = HttpResponse(html, content_type='text/html')


    if request.POST['action'] == 'save':
        if text_type == '0':
            response["Content-Disposition"] = "attachment; filename=export_citation.txt"
        else:
            open(os.path.join(MEDIA_ROOT, 'data/export_citation.html'), 'w').write(html.encode('UTF-8'))

            try:
                subprocess.check_call('cd %s/data && pandoc -f html -t docx -o export_citation.docx export_citation.html' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                send_error_slack(traceback.format_exc(), 'Export Citations', 'export_citation', 'log_django.log')

            lines = open(os.path.join(MEDIA_ROOT, 'data/export_citation.docx'), 'r').readlines()
            response = HttpResponse(lines, content_type='application/msword')
            response["Content-Disposition"] = "attachment; filename=export_citation.docx"
    return response




