sudo rm media/js/admin/min/*.min.js
java -jar ../yuicompressor-2.4.8.jar -o '.js$:.min.js' media/js/admin/*.js
mv media/js/admin/*.min.js media/js/admin/min/

sudo rm media/js/group/min/*.min.js
java -jar ../yuicompressor-2.4.8.jar -o '.js$:.min.js' media/js/group/*.js
mv media/js/group/*.min.js media/js/group/min/

sudo rm media/js/suit/min/*.min.js
java -jar ../yuicompressor-2.4.8.jar -o '.js$:.min.js' media/js/suit/*.js
mv media/js/suit/*.min.js media/js/suit/min/

sudo rm media/css/min/*.min.css
java -jar ../yuicompressor-2.4.8.jar -o '.css$:.min.css' media/css/*.css
rm media/css/*.min.min.css
mv media/css/*.min.css media/css/min/
mv media/css/min/bootstrap.min.css media/css/
mv media/css/min/fullcalendar.min.css media/css/
