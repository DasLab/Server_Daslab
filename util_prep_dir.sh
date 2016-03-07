mkdir backup
mkdir config/sys

mkdir cache
mkdir cache/aws cache/dropbox cache/ga cache/git cache/slack
touch cache/log_alert_admin.log cache/log_cron.log cache/log_django.log
touch cache/log_cron_backup.log cache/log_cron_bday.log cache/log_cron_cache.log cache/log_cron_duty.log cache/log_cron_gdrive.log cache/log_cron_meeting.log cache/log_cron_report.log cache/log_cron_version.log
touch cache/stat_backup.json cache/stat_sys.json cache/stat_ver.json

cp -n config/cron.conf.example config/cron.conf
cp -n config/env.conf.example config/env.conf
cp -n config/group.conf.example config/group.conf
cp -n config/oauth.conf.example config/oauth.conf
cp -n config/t47_dev.py.example config/t47_dev.py

mkdir data
mkdir data/news_img data/ppl_img data/pub_data data/pub_img data/pub_pdf data/rot_data data/rot_ppt data/spe_ppt

mkdir media/css/min
mkdir media/js/admin/min media/js/group/min media/js/suit/min

./util_chmod.sh
