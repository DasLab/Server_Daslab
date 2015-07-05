import datetime
import os

from django.core.mail import send_mail

from src.settings import MEDIA_ROOT, CRONJOBS, EMAIL_NOTIFY, EMAIL_HOST_USER


def send_notify_emails(msg_subject, msg_content):
	send_mail(msg_subject, msg_content, EMAIL_HOST_USER, [EMAIL_NOTIFY])


def get_date_time(keyword):
	t_cron = [c[0] for c in CRONJOBS if c[1].find(keyword) != -1][0]
	d_cron = ['Sun', 'Mon', 'Tues', 'Wednes', 'Thurs', 'Fri', 'Satur'][int(t_cron.split(' ')[-1])]
	t_cron = datetime.datetime.strptime(' '.join(t_cron.split(' ')[0:2]),'%M %H').strftime('%I:%M%p')
	t_now = datetime.datetime.now().strftime('%b %d %Y (%a) @ %H:%M:%S')
	return(t_cron, d_cron, t_now)


def backup_weekly():
	os.popen('cd %s && python util_backup.py' % MEDIA_ROOT)
	(t_cron, d_cron, t_now) = get_date_time('backup')
	send_notify_emails('[System] {daslab.stanford.edu} Weekly Backup Notice', 'This is an automatic email notification for the success of scheduled weekly backup of the DasLab Website database and static contents.\n\nThe crontab job is scheduled at %s (UTC) on every %sday.\n\nThe last system backup was performed at %s (PDT).\n\n' % (t_cron, d_cron, t_now))

def gdrive_weekly():
	os.popen('cd %s && python util_gdrive_sync.py' % MEDIA_ROOT)
	(t_cron, d_cron, t_now) = get_date_time('grive')
	send_notify_emails('[System] {daslab.stanford.edu} Weekly Sync Notice', 'This is an automatic email notification for the success of scheduled weekly sync of the DasLab Website backup contents to Google Drive account.\n\nThe crontab job is scheduled at %s (UTC) on every %sday.\n\nThe last system backup was performed at %s (PDT).\n\n' % (t_cron, d_cron, t_now))

