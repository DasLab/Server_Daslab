sudo usermod -a -G www-data ubuntu

sudo chgrp -R www-data *
# sudo chgrp -R ubuntu cache
sudo chown -R ubuntu *.py *.md *.txt src media config .gitignore
sudo chown -R www-data backup data cache

sudo chmod 640 *.py* *.md *.txt .gitignore
sudo chmod 640 src/*.py* src/management/* src/management/commands/* src/templatetags/*
sudo chmod 750 src src/management src/management/commands src/templatetags
sudo chmod 640 media/css/* media/fonts/* media/html/* media/fonts/GillSans/* media/fonts/Helvetica/* media/js/* media/js/admin/* media/js/group/* media/js/suit/* media/_old/* media/swf/*
sudo chmod 750 media/css media/fonts media/fonts/GillSans media/fonts/Helvetica media/html media/js media/js/admin media/js/group media/js/suit media/_old media/swf media
sudo chmod 640 media/images/*.*g* media/images/contact/* media/images/group/* media/images/group/clock/* media/images/group/baking/* media/images/home/* media/images/news/* media/images/people/* media/images/publications/* media/images/research/* media/images/resources/* media/images/icons/*
sudo chmod 750 media/images media/images/contact media/images/group media/images/group/clock media/images/group/baking media/images/home media/images/news media/images/people media/images/publications media/images/research media/images/resources media/images/icons
sudo chmod 640 media/admin/*.html media/admin/img/*.*g* media/admin/img/gis/* media/admin/img/filemanager/* media/admin/js/*.js 
sudo chmod 750 media/admin media/admin/img media/admin/img/gis media/admin/img/filemanager media/admin/js 

sudo chmod 640 media/css/min/* media/js/group/min/* media/js/admin/min/* media/js/suit/min/*
sudo chmod 750 media/css/min media/js/group/min media/js/admin/min media/js/suit/min

sudo chmod 660 backup/* cache/* cache/aws/* cache/slack/* cache/git/* cache/ga/* cache/dropbox/*
sudo chmod 770 backup cache cache/aws cache/slack cache/git cache/ga cache/dropbox
sudo chmod 640 data/*.pdf data/news_img/* data/_old/* data/ppl_img/* data/pub_data/* data/pub_img/* data/pub_pdf/* data/rot_data/* data/rot_ppt/* data/spe_ppt/*
sudo chmod 750 data data/news_img data/_old data/ppl_img data/pub_data data/pub_img data/pub_pdf data/rot_data data/rot_ppt data/spe_ppt

sudo chmod 640 config/*.py* config/*.example config/*.conf
sudo chown www-data config/cron.conf config/bot.conf
sudo chmod 750 config

sudo chgrp -R ubuntu *.sh
sudo chown -R ubuntu *.sh
sudo chmod -R 700 *.sh
