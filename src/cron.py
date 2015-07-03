import os
import datetime

from src.settings import MEDIA_ROOT

def backup_weekly():
	print "!cron!"
	os.popen('touch ~/%s.txt' % datetime.now().strftime('%H-%M-%S'))
	# os.popen('cd %s && python util_backup.py' % MEDIA_ROOT)


