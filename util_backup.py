import os
import subprocess
import sys
import time

t0 = time.time()
sys.path.append(os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings") 

from src.settings import *

flag = False
t = time.time()
print "#1: Backing up MySQL database..."
try:
	subprocess.check_call('mysqldump --quick %s -u %s -p%s > %s/backup/backup_mysql' % (env.db()['NAME'], env.db()['USER'], env.db()['PASSWORD'], MEDIA_ROOT), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	subprocess.check_call('gzip -f %s/backup/backup_mysql' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
	print "    \033[41mERROR\033[0m: Failed to dump \033[94mMySQL\033[0m database."
	flag = True
else:
	print "    \033[92mSUCCESS\033[0m: \033[94mMySQL\033[0m database dumped."
print "Time elapsed: %.1f s." % (time.time() - t)

t = time.time()
print "#2: Backing up static files..."
try:
	subprocess.check_call('cd %s && tar zcf backup/backup_static.tgz data/' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
	print "    \033[41mERROR\033[0m: Failed to archive \033[94mstatic\033[0m files."
	flag = True
else:
	print "    \033[92mSUCCESS\033[0m: \033[94mstatic\033[0m files synced."
print "Time elapsed: %.1f s." % (time.time() - t)

t = time.time()
print "#3: Backing up apache2 settings..."
try:
	subprocess.check_call('cp -r /etc/apache2 %s/backup' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	subprocess.check_call('cd %s/backup && tar zcf backup_apache.tgz apache2/' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	subprocess.check_call('rm -rf %s/backup/apache2' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
	print "    \033[41mERROR\033[0m: Failed to archive \033[94mapache2\033[0m settings."
	flag = True
else:
	print "    \033[92mSUCCESS\033[0m: \033[94mapache2\033[0m settings saved."
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
