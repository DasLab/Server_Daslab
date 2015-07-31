sudo usermod -a -G www-data ubuntu

sudo chgrp -R www-data *
sudo chown -R ubuntu *.py *.md *.txt src media config .gitignore
sudo chown -R www-data backup data

sudo chmod 640 *.py* *.md *.txt .gitignore
sudo chmod 640 src/*.py* src/templatetags/*
sudo chmod 750 src src/templatetags
sudo chmod 640 media/css/* media/fonts/* media/html/* media/js/* media/_old/* media/swf/*
sudo chmod 750 media/css media/fonts media/html media/js media/_old media/swf media
sudo chmod 640 media/images/*.*g* media/images/contact/* media/images/group/* media/images/home/* media/images/news/* media/images/people/* media/images/publications/* media/images/research/* media/images/resources/*
sudo chmod 750 media/images media/images/contact media/images/group media/images/home media/images/news media/images/people media/images/publications media/images/research media/images/resources
sudo chmod 640 media/admin/*.html media/admin/css/* media/admin/img/*.*g* media/admin/img/gis/* media/admin/img/filemanager/* media/admin/js/*.js media/admin/js/custom/* media/admin/js/filemanager/* media/admin/js/suit/*
sudo chmod 750 media/admin media/admin/css media/admin/img media/admin/img/gis media/admin/img/filemanager media/admin/js media/admin/js/custom media/admin/js/filemanager media/admin/js/suit

sudo chmod 640 backup/*
sudo chmod 750 backup
sudo chmod 640 data/*.txt data/*.log data/*.pdf data/news_img/* data/_old/* data/ppl_img/* data/pub_data/* data/pub_img/* data/pub_pdf/* data/rot_data/* data/rot_ppt/* data/spe_ppt/*
sudo chmod 750 data data/news_img data/_old data/ppl_img data/pub_data data/pub_img data/pub_pdf data/rot_data data/rot_ppt data/spe_ppt

sudo chmod 640 config/*.py* config/*.example config/*.conf
sudo chown www-data config/cron.conf 
sudo chmod 750 config

sudo chgrp -R ubuntu *.sh
sudo chown -R ubuntu *.sh
sudo chmod -R 700 *.sh
