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

flag = False
t = time.time()
print "#1: Restoring MySQL database..."
try:
    subprocess.check_call('gunzip < %s/backup/backup_mysql.gz | mysql -u %s -p%s %s' % (MEDIA_ROOT, env.db()['USER'], env.db()['PASSWORD'], env.db()['NAME']), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
    print "    \033[41mERROR\033[0m: Failed to overwrite \033[94mMySQL\033[0m database."
    print traceback.format_exc()
    flag = True
else:
    print "    \033[92mSUCCESS\033[0m: \033[94mMySQL\033[0m database overwritten."
print "Time elapsed: %.1f s." % (time.time() - t)

t = time.time()
print "#2: Restoring static files..."
try:
    subprocess.check_call('rm -rf %s/backup/data' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    subprocess.check_call('cd %s/backup && tar zvxf backup_static.tgz' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    subprocess.check_call('rm -rf %s/data' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    subprocess.check_call('mv %s/backup/data %s/' % (MEDIA_ROOT, MEDIA_ROOT), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    subprocess.check_call('rm -rf %s/backup/data' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if not DEBUG:
        subprocess.check_call('%s/util_chmod.sh' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
    print "    \033[41mERROR\033[0m: Failed to restore \033[94mstatic\033[0m files."
    print traceback.format_exc()
    flag = True
else:
    print "    \033[92mSUCCESS\033[0m: \033[94mstatic\033[0m files overwritten."
print "Time elapsed: %.1f s." % (time.time() - t)

t = time.time()
print "#3: Restoring apache2 settings..."
try:
    subprocess.check_call('rm -rf %s/backup/apache2' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    subprocess.check_call('cd %s/backup && tar zvxf backup_apache.tgz' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    subprocess.check_call('rm -rf /etc/apache2', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    subprocess.check_call('mv %s/backup/apache2 /etc/apache2 ' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    subprocess.check_call('rm -rf %s/backup/apache2' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if not DEBUG:
        subprocess.check_call('apache2ctl restart', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
    print "    \033[41mERROR\033[0m: Failed to restore \033[94mapache2\033[0m settings."
    print traceback.format_exc()
    flag = True
else:
    print "    \033[92mSUCCESS\033[0m: \033[94mapache2\033[0m settings overwritten."
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
