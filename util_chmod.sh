sudo chown -R ubuntu *.py *.md *.txt src media config
sudo chown -R www-data backup data

sudo chmod 644 src/*.py* src/templatetags/*
sudo chmod 755 src src/templatetags
sudo chmod 644 media/css/* media/fonts/* media/html/* media/js/* media/_old/* media/swf/*
sudo chmod 755 media/css media/fonts media/html media/js media/_old media/swf
sudo chmod 644 media/images/*.jpg media/images/*.png media/images/contact/* media/images/group/* media/images/home/* media/images/news/* media/images/people/* media/images/publications/* media/images/research/* media/images/resources/*
sudo chmod 755 media/images media/images/contact media/images/group media/images/home media/images/news media/images/people media/images/publications media/images/research media/images/resources
sudo chmod 644 media/admin/*.html media/admin/css/* media/admin/img/*.gif media/admin/img/*.png media/admin/img/gis/* media/admin/img/filemanager/* media/admin/js/*.js media/admin/js/custom/* media/admin/js/filemanager/* media/admin/js/suit/*
sudo chmod 755 media/admin media/admin/css media/admin/img media/admin/img/gis media/admin/img/filemanager media/admin/js media/admin/js/custom media/admin/js/filemanager media/admin/js/suit

sudo chmod 644 backup/*
sudo chmod 755 backup
sudo chmod 644 data/*.txt data/*.pdf data/news_img/* data/_old/* data/ppl_img/* data/pub_data/* data/pub_img/* data/pub_pdf/* data/rot_data/* data/rot_ppt/* data/spe_ppt/*
sudo chmod 755 data data/news_img data/_old data/ppl_img data/pub_data data/pub_img data/pub_pdf data/rot_data data/rot_ppt data/spe_ppt

