from datetime import datetime, timedelta
import os
import simplejson
import subprocess
import sys
import textwrap
import urllib
import urllib2

from django.core.management import call_command
from django.http import HttpResponse

from src.settings import *
from src.models import BackupForm, Publication


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
    if not DEBUG: gdrive_dir = 'cd %s' % APACHE_ROOT
    ver += '~|~'.join(subprocess.Popen("%s && drive list -q \"title contains 'DasLab_'\"" % gdrive_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[4:])

    f = open(os.path.join(MEDIA_ROOT, 'data/stat_backup.txt'), 'w')
    f.write(ver)
    f.close()
    subprocess.Popen('rm %s' % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def get_backup_form():
    cron = subprocess.Popen('crontab -l | cut -d" " -f1-5', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()
    try:
        day_backup = cron[4]
        day_upload = cron[9]
        time_backup = '%02d:%02d' % (int(cron[1]), int(cron[0]))
        time_upload = '%02d:%02d' % (int(cron[6]), int(cron[5]))
    except:
        time_backup = time_upload = day_backup = day_upload = ''

    json = {'day_backup':day_backup, 'day_upload':day_upload, 'time_backup':time_backup, 'time_upload':time_upload}
    return simplejson.dumps(json)


def set_backup_form(request):
    time_backup = request.POST['time_backup'].split(':')
    time_upload = request.POST['time_upload'].split(':')
    day_backup = request.POST['day_backup']
    day_upload = request.POST['day_upload']

    cron_backup = '%s %s * * %s' % (time_backup[1], time_backup[0], day_backup)
    cron_upload = '%s %s * * %s' % (time_upload[1], time_upload[0], day_upload)

    f = open('%s/config/cron.conf' % MEDIA_ROOT, 'r')
    lines = f.readlines()
    f.close()

    index =  [i for i, line in enumerate(lines) if 'src.cron.backup_weekly' in line or 'src.cron.gdrive_weekly' in line or 'KEEP_BACKUP' in line]
    lines[index[0]] = '\t\t["%s", "src.cron.backup_weekly"],\n' % cron_backup
    lines[index[1]] = '\t\t["%s", "src.cron.gdrive_weekly"]\n' % cron_upload
    lines[index[2]] = '\t"KEEP_BACKUP": %s\n' % request.POST['keep']

    f = open('%s/config/cron.conf' % MEDIA_ROOT, 'w')
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


def restyle_apache():
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    apache_url = "http://daslab.stanford.edu/server-status/"
    password_mgr.add_password(None, apache_url, env('APACHE_USER'), env('APACHE_PASSWORD'))
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)

    request = urllib2.urlopen(apache_url)
    response = request.read().split('\n')

    title = 'Apache Server Status for <code>daslab.stanford.edu</code> (via <kbd>%s</kbd> )' % response[4].replace(')</h1>', '')[-13:]
    ver = response[6].replace('<dl><dt>Server Version: Apache/', '').replace('(Ubuntu) mod_wsgi/', '').replace('Python/', '').replace('</dt>', '').split()
    mpm = response[7].replace('<dt>Server MPM: ', '').replace('</dt>', '')
    time_build = datetime.strftime(datetime.strptime(response[8].replace('<dt>Server Built: ', ''), '%b %d %Y %H:%M:%S'), '%Y-%m-%d (%A) %I:%M:%S %p (PDT)')
    time_current = datetime.strftime(datetime.strptime(response[10].replace('<dt>Current Time: ', '').replace('</dt>', ''), '%A, %d-%b-%Y %H:%M:%S %Z'), '%Y-%m-%d (%A) %I:%M:%S %p (PDT)')
    time_restart = datetime.strftime(datetime.strptime(response[11].replace('<dt>Restart Time: ', '').replace('</dt>', ''), '%A, %d-%b-%Y %H:%M:%S %Z'), '%Y-%m-%d (%A) %I:%M:%S %p (PDT)')
    time_up = response[14].replace('<dt>Server uptime:  ', '').replace('</dt>', '').replace('hours', '<i>h</i>').replace('hour', '<i>h</i>').replace('minutes', '<i>min</i>').replace('minute', '<i>min</i>').replace('seconds', '<i>s</i>').replace('second', '<i>s</i>')

    server_load = response[15].replace('<dt>Server load: ', '').replace('</dt>', '').replace(' ', ' / ')
    total = response[16].replace('<dt>Total accesses: ', '').replace(' - Total Traffic:', '').replace('</dt>', '').split()
    cpu = response[17].replace('<dt>CPU Usage: ', '').replace('% CPU load</dt>', '').replace(' -', '').split()
    cpu_usage = '%.2f / %.2f / %.2f / %.2f' % (float(cpu[0][1:]), float(cpu[1][1:]), float(cpu[2][2:]), float(cpu[3][2:]))
    cpu_load = '%1.4f' % float(cpu[4])
    traffic = response[18].replace('<dt>', '').replace('B/request</dt>', '').replace('requests/sec -', '').replace('B/second -', '').split()
    if traffic[-1] in ('k', 'M', 'G'): 
        traffic = '%1.2f / %.1f / %s' % (float(traffic[0]), float(traffic[-2]), traffic[-1])
    else:
        traffic = '%1.2f / %.1f' % (float(traffic[0]), float(traffic[-1]))
    workers = response[19].replace('<dt>', '').replace('requests currently being processed, ', '').replace('idle workers</dt>', '').split()
    worker = '<p style="margin-bottom:0px;">' + '</p><p style="margin-bottom:0px;">'.join(textwrap.wrap(''.join(response[20:22]).replace('</dl><pre>', '').replace('</pre>', ''), 30)).replace('.', '<span class="label label-primary">.</span>').replace('_', '<span class="label label-inverse">_</span>').replace('S', '<span class="label label-default">S</span>').replace('R', '<span class="label label-violet">R</span>').replace('W', '<span class="label label-info">W</span>').replace('K', '<span class="label label-success">K</span>').replace('D', '<span class="label label-warning">D</span>').replace('C', '<span class="label label-danger">C</span>').replace('L', '<span class="label label-orange">L</span>').replace('G', '<span class="label label-green">G</span>').replace('I', '<span class="label label-brown">I</span>') + '</p>'

    table = ''.join(response[40:len(response)-17]).replace('<td>.</td>', '<td><span class="label label-primary">.</span></td>').replace('<td>_</td>', '<td><span class="label label-inverse">_</span></td>').replace('<td><b>S</b></td>', '<td><span class="label label-default">S</span></td>').replace('<td><b>R</b></td>', '<td><span class="label label-violet">R</span></td>').replace('<td><b>W</b></td>', '<td><span class="label label-info">W</span></td>').replace('<td><b>K</b></td>', '<td><span class="label label-success">K</span></td>').replace('<td><b>D</b></td>', '<td><span class="label label-warning">D</span></td>').replace('<td><b>C</b></td>', '<td><span class="label label-danger">C</span></td>').replace('<td><b>L</b></td>', '<td><span class="label label-orange">L</span></td>').replace('<td><b>G</b></td>', '<td><span class="label label-green">G</span></td>').replace('<td><b>I</b></td>', '<td><span class="label label-brown">I</span></td>')
    port = response[len(response)-3].replace('</address>', '')[-3:]

    json = {'title':title, 'ver_apache':ver[0], 'ver_wsgi':ver[1], 'ver_python':ver[2], 'mpm':mpm, 'time_build':time_build, 'time_current':time_current, 'time_restart':time_restart, 'time_up':time_up, 'server_load':server_load, 'total_access':total[0], 'total_traffic':'%s %s' % (total[1], total[2]), 'cpu_load':cpu_load, 'cpu_usage':cpu_usage, 'traffic':traffic, 'idle':workers[1], 'processing':workers[0], 'worker':worker, 'table':table, 'port':port}
    return simplejson.dumps(json)
    

def ga_stats():
    access_token = subprocess.Popen('curl --silent --request POST "https://www.googleapis.com/oauth2/v3/token" --data "refresh_token=%s" --data "client_id=%s" --data "client_secret=%s" --data "grant_type=refresh_token"' % (REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
    access_token = simplejson.loads(access_token)['access_token']

    stats = {'access_token':access_token}
    for i in ('sessionDuration', 'bounceRate', 'pageviewsPerSession', 'pageviews', 'sessions', 'users'):
        temp = subprocess.Popen('curl --silent --request GET "https://www.googleapis.com/analytics/v3/data/ga?ids=ga%s%s&start-date=30daysAgo&end-date=yesterday&metrics=ga%s%s&access_token=%s"' % (urllib.quote(':'), GA_ID, urllib.quote(':'), i, access_token), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
        temp = simplejson.loads(temp)['rows'][0][0]
        temp_prev = subprocess.Popen('curl --silent --request GET "https://www.googleapis.com/analytics/v3/data/ga?ids=ga%s%s&start-date=60daysAgo&end-date=30daysAgo&metrics=ga%s%s&access_token=%s"' % (urllib.quote(':'), GA_ID, urllib.quote(':'), i, access_token), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
        temp_prev = simplejson.loads(temp_prev)['rows'][0][0]

        if i in ('bounceRate', 'pageviewsPerSession'):
            temp_prev = '%.2f' % (float(temp) - float(temp_prev))
            temp = '%.2f' % float(temp)
        elif i == 'sessionDuration':
            temp_prev = str(timedelta(seconds=(int(float(temp) / 1000) - int(float(temp_prev) / 1000))))
            temp = str(timedelta(seconds=int(float(temp) / 1000)))
        else:
            temp_prev = '%d' % (int(temp) - int(temp_prev))
            temp = '%d' % int(temp)
        stats[i] = temp
        stats[i + '_prev'] = temp_prev
    return stats


def export_citation(request):
    is_order_number = 'order_number' in request.POST
    is_quote_title = 'quote_title' in request.POST
    is_double_space = 'double_space' in request.POST
    is_include_preprint = 'include_preprint' in request.POST

    text_type = request.POST['text_type']
    year_start = int(request.POST['year_start'])
    number_order = (request.POST['number_order'] == '1')
    sort_order = 'display_date'
    if request.POST['sort_order'] == '1': sort_order = '-' + sort_order

    publications = Publication.objects.filter(year__gte=year_start).order_by(sort_order)
    if not is_include_preprint: publications = publications.filter(preprint=False)

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
        is_bold_author = 'bold_author' in request.POST
        is_bold_year = 'bold_year' in request.POST
        is_underline_title = 'underline_title' in request.POST
        is_italic_journal = 'italic_journal' in request.POST
        is_bold_volume = 'bold_volume' in request.POST

        html = ''
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

        response = HttpResponse(html, content_type='text/html')
        

    if request.POST['action'] == 'save':
        if text_type == '0':
            response["Content-Disposition"] = "attachment; filename=export_citation.txt"
        else:
            f = open(os.path.join(MEDIA_ROOT, 'data/export_citation.html'), 'w')
            f.write(html.encode('UTF-8'))
            f.close()

            os.popen('cd %s/data && pandoc -f html -t docx -o export_citation.docx export_citation.html' % MEDIA_ROOT)

            f = open(os.path.join(MEDIA_ROOT, 'data/export_citation.docx'), 'r')
            lines = f.readlines()
            f.close()

            response = HttpResponse(lines, content_type='application/msword')
            response["Content-Disposition"] = "attachment; filename=export_citation.docx"
    return response



