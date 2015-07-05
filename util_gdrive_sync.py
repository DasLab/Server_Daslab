import os
import subprocess
import sys
import datetime

sys.path.append(os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings") 

from src.settings import *

t = datetime.datetime.now().strftime('%Y%m%d')

print "#1: Uploading MySQL database..."
os.popen('cd %s && drive upload -f ../backup_mysql.gz -t DasLab_%s_mysql.gz' % (MEDIA_ROOT, t))
print "    \033[92mSUCCESS\033[0m: \033[94mMySQL\033[0m database uploaded."

print "#2: Uploading static files..."
os.popen('cd %s && drive upload -f ../backup_static.tgz -t DasLab_%s_static.tgz' % (MEDIA_ROOT, t))
print "    \033[92mSUCCESS\033[0m: \033[94mstatic\033[0m files uploaded."

print "#3: Uploading apache2 settings..."
os.popen('cd %s && drive upload -f ../backup_apache.tgz -t DasLab_%s_apache.tgz' % (MEDIA_ROOT, t))
print "    \033[92mSUCCESS\033[0m: \033[94mapache2\033[0m settings uploaded."


print "#4: Removing obsolete backups..."

old = (datetime.date.today() - datetime.timedelta(days=KEEP_BACKUP)).strftime('%Y-%m-%dT00:00:00')

list_mysql = subprocess.Popen("drive list -q \"title contains 'DasLab' and title contains '_mysql.gz' and modifiedDate <= '%s'\"| awk '{ printf $1\" \"}'" % old, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[1:]
list_static = subprocess.Popen("drive list -q \"title contains 'DasLab' and title contains '_static.tgz' and modifiedDate <= '%s'\"| awk '{ printf $1\" \"}'" % old, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[1:]
list_apache = subprocess.Popen("drive list -q \"title contains 'DasLab' and title contains '_apache.tgz' and modifiedDate <= '%s'\"| awk '{ printf $1\" \"}'" % old, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[1:]
list_all = list_mysql + list_static + list_apache

for id in list_all:
	os.popen('drive info -i %s' % id)
	print
	os.popen('drive delete -i %s' % id)

print "    \033[92mSUCCESS\033[0m: \033[94m%s\033[0m obsolete backup files removed." % len(list_all)


print "All done!"
