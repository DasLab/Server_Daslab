from datetime import datetime, timedelta
import os
import smtplib
import sys
import time
import traceback

sys.path.append(os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings") 

from src.settings import *
from src.cron import send_notify_emails, send_notify_slack


t0 = time.time()
print time.ctime()

try:
    lines = open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'r').readlines()
    lines = ''.join(lines)
    if not IS_SLACK:
        send_notify_emails('[System] {daslab.stanford.edu} Weekly Error Report', 'This is an automatic email notification for the aggregated weekly error report. The following error occurred:\n\n\n%s\n\n\nDasLab Website Admin' % (lines))
        open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'w').write('')

except:
    err = traceback.format_exc()
    ts = '%s\t\t%s\n' % (time.ctime(), sys.argv[0])
    open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
    open('%s/cache/log_cron_report.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
    if IS_SLACK: send_notify_slack(SLACK['ADMIN_ID'], '*`ERROR`*: *%s* @ _%s_\n>```%s```\n' % (sys.argv[0], time.ctime(), err))
    print "Finished with \033[41mERROR\033[0m!"
    print "Time elapsed: %.1f s." % (time.time() - t0)
    sys.exit(1)

print "Finished with \033[92mSUCCESS\033[0m!"
print "Time elapsed: %.1f s." % (time.time() - t0)
sys.exit(0)
