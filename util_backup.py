import os
import sys

sys.path.append(os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings") 

from src.settings import *


print "#1: Backing up MySQL database..."
os.popen('mysqldump --quick daslab -u root -pbeckman | gzip > %s/../mysql_dump.gz' % MEDIA_ROOT)
print "    \033[92mSUCCESS\033[0m: \033[94mMySQL\033[0m database dumped."

print "#2: Backing up static files..."
os.popen('cd %s && tar zcf ../data_backup.tgz data/' % MEDIA_ROOT)
print "    \033[92mSUCCESS\033[0m: \033[94mstatic\033[0m files synced."

print "#3: Backing up apache2 settings..."
os.popen('cp -r /etc/apache2 %s' % MEDIA_ROOT)
os.popen('cd %s && tar zcf ../apache2_backup.tgz apache2/' % MEDIA_ROOT)
os.popen('rm -rf %s/apache2' % MEDIA_ROOT)
print "    \033[92mSUCCESS\033[0m: \033[94mapache2\033[0m settings saved."

print "All done!"
