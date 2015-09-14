import datetime
import os
import subprocess
import sys
import time
import traceback

t0 = time.time()
print time.ctime()
sys.path.append(os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings") 

from src.settings import *


d = time.strftime('%Y%m%d') #datetime.datetime.now().strftime('%Y%m%d')
gdrive_dir = 'echo'
if not DEBUG: gdrive_dir = 'cd %s' % APACHE_ROOT
prefix = ''
if DEBUG: prefix = '_DEBUG'

flag = False
t = time.time()
print "#1: Uploading MySQL database..."
try:
    subprocess.check_call('%s && drive upload -f %s/backup/backup_mysql.gz -t DasLab_%s_mysql%s.gz' % (gdrive_dir, MEDIA_ROOT, d, prefix), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
    print "    \033[41mERROR\033[0m: Failed to upload \033[94mMySQL\033[0m database."
    print traceback.format_exc()
    flag = True
else:
    print "    \033[92mSUCCESS\033[0m: \033[94mMySQL\033[0m database uploaded."
print "Time elapsed: %.1f s." % (time.time() - t)

t = time.time()
print "#2: Uploading static files..."
try:
    subprocess.check_call('%s && drive upload -f %s/backup/backup_static.tgz -t DasLab_%s_static%s.tgz' % (gdrive_dir, MEDIA_ROOT, d, prefix), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
    print "    \033[41mERROR\033[0m: Failed to upload \033[94mstatic\033[0m files."
    print traceback.format_exc()
    flag = True
else:
    print "    \033[92mSUCCESS\033[0m: \033[94mstatic\033[0m files uploaded."
print "Time elapsed: %.1f s." % (time.time() - t)

t = time.time()
print "#3: Uploading apache2 settings..."
try:
    subprocess.check_call('%s && drive upload -f %s/backup/backup_apache.tgz -t DasLab_%s_apache%s.tgz' % (gdrive_dir, MEDIA_ROOT, d, prefix), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
    print "    \033[41mERROR\033[0m: Failed to upload \033[94mapache2\033[0m settings."
    print traceback.format_exc()
    flag = True
else:
    print "    \033[92mSUCCESS\033[0m: \033[94mapache2\033[0m settings uploaded."
print "Time elapsed: %.1f s." % (time.time() - t)


t = time.time()
print "#4: Removing obsolete backups..."
old = (datetime.date.today() - datetime.timedelta(days=KEEP_BACKUP)).strftime('%Y-%m-%dT00:00:00')

list_mysql = subprocess.Popen("%s && drive list -q \"title contains 'DasLab' and (title contains '_mysql.gz' or title contains '_mysql_DEBUG.gz') and modifiedDate <= '%s'\"| awk '{ printf $1\" \"}'" % (gdrive_dir, old), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[1:]
list_static = subprocess.Popen("%s && drive list -q \"title contains 'DasLab' and (title contains '_static.tgz' or title contains '_static_DEBUG.tgz') and modifiedDate <= '%s'\"| awk '{ printf $1\" \"}'" % (gdrive_dir, old), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[1:]
list_apache = subprocess.Popen("%s && drive list -q \"title contains 'DasLab' and (title contains '_apache.tgz' or title contains '_apache_DEBUG.tgz') and modifiedDate <= '%s'\"| awk '{ printf $1\" \"}'" % (gdrive_dir, old), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[1:]
list_all = list_mysql + list_static + list_apache

for id in list_all:
    try:
        subprocess.check_call('%s && drive info -i %s' % (gdrive_dir, id), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print
        subprocess.check_call('%s && drive delete -i %s' % (gdrive_dir, id), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print "    \033[41mERROR\033[0m: Failed to remove obsolete \033[94mbackup\033[0m files."
        print traceback.format_exc()
        flag = True

if not flag: print "    \033[92mSUCCESS\033[0m: \033[94m%s\033[0m obsolete backup files removed." % len(list_all)
print "Time elapsed: %.1f s." % (time.time() - t)
print

if flag:
    print "Finished with errors!"
    print "Time elapsed: %.1f s." % (time.time() - t0)
    sys.exit(1)
else:
    print "All done successfully!"
    print "Time elapsed: %.1f s." % (time.time() - t0)
    sys.exit(0)

