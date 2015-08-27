echo "$(tput setab 1) ubuntu $(lsb_release -a | head -2 | tail -1 | sed 's/.*Ubuntu //g') | \
linux $(uname -r | sed 's/[a-z]//g' | sed 's/\-//g') | \
screen $(screen --version | sed 's/.*version//g' | sed 's/(.*//g' | sed 's/[a-z ]//g') | \
bash $(bash --version | head -1 | sed 's/.*version//g' | sed 's/-release.*//g' | sed 's/[ ()]//g') | \
ssh $(cut -d$'\t' -f17 data/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" > ~/.ver_txt

echo -n "$(tput setab 172) clang $(clang --version | head -1 | sed 's/.*version //g' | sed 's/-.*//g') | \
gcc $(gcc --version | head -1 | sed 's/.*) //g') | \
make $(make --version | head -1 | sed 's/.*Make//g' | sed 's/ //g') | \
cmake $(cmake --version | head -1 | sed 's/.*version//g' | sed 's/ //g') | \
ninja $(ninja --version) |$(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 8) git $(cut -d$'\t' -f18 data/stat_sys.txt | sed 's/ $*//') | \
pip $(cut -d$'\t' -f23 data/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 11)$(tput setaf 16) python $(cut -d$'\t' -f2 data/stat_sys.txt | sed 's/ $*//') | \
java $(javac -version 2> temp.txt && sed 's/.*javac //g' temp.txt | sed 's/_/./g') | \
perl $(perl --version > temp.txt && head -2 temp.txt | tail -1 | sed 's/).*//g' | sed 's/.*(//g' | sed 's/[a-z]//g') | \
php $(php --version | head -1 | sed 's/\-.*//g' | sed 's/[A-Z ]//g') | \
ruby $(ruby --version | sed 's/.*ruby //g' | sed 's/ (.*//g' | sed 's/[a-z]/./g') | \
go $(go version | sed 's/.*version go//g' | sed 's/ .*//g') $(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 2) coreutils $(tty --version | head -1 | sed 's/.*) //g') | \
wget $(wget --version | head -1 | sed 's/.*Wget//g' | sed 's/built.*//g' | sed 's/ //g') | \
tar $(tar --version | head -1 | sed 's/.*)//g' | sed 's/-.*//g' | sed 's/ //g') | \
ghostscript $(gs --version) | \
imagemagick $(mogrify -version | head -1 | sed 's/\-.*//g' | sed 's/.*ImageMagick //g') $(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 22) apache $(cut -d$'\t' -f15 data/stat_sys.txt | sed 's/ $*//') | \
curl $(cut -d$'\t' -f22 data/stat_sys.txt | sed 's/ $*//') | \
gdrive $(cut -d$'\t' -f20 data/stat_sys.txt | sed 's/ $*//') | \
pandoc $(cut -d$'\t' -f21 data/stat_sys.txt | sed 's/ $*//') | \
gitinspector $(cut -d$'\t' -f19 data/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 39) $(python -c "import celery; import virtualenv; import simplejson; import Tkinter; import setuptools; \
print 'tkinter', Tkinter.Tcl().eval('info patchlevel'), '| virtualenv', virtualenv.__version__, '| setuptools', setuptools.__version__, '| simplejson', simplejson.__version__, '| celery %d.%d.%d' %(celery.VERSION.major, celery.VERSION.minor, celery.VERSION.micro)") $(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 20) jquery $(cut -d$'\t' -f9 data/stat_sys.txt | sed 's/ $*//') | \
bootstrap $(cut -d$'\t' -f10 data/stat_sys.txt | sed 's/ $*//') | \
swfobject $(cut -d$'\t' -f11 data/stat_sys.txt | sed 's/ $*//') | \
moment $(cut -d$'\t' -f13 data/stat_sys.txt | sed 's/ $*//') | \
fullcalendar $(cut -d$'\t' -f12 data/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 55) crontab $(cut -d$'\t' -f6 data/stat_sys.txt | sed 's/ $*//') | \
environ $(cut -d$'\t' -f7 data/stat_sys.txt | sed 's/ $*//') | \
suit $(cut -d$'\t' -f4 data/stat_sys.txt | sed 's/ $*//') | \
adminplus $(cut -d$'\t' -f5 data/stat_sys.txt | sed 's/ $*//') | \
filemanager $(cut -d$'\t' -f8 data/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" >> ~/.ver_txt

echo -n "$(tput setab 171) nano $(nano --version | head -1 | sed 's/.*version //g' | sed 's/(.*//g')| \
vim $(vim --version | head -1 | sed 's/.*IMproved//g' | sed 's/(.*//g' | sed 's/ //g') | \
emacs $(emacs --version | head -1 | sed 's/.*Emacs //g') | \
mysql $(cut -d$'\t' -f14 data/stat_sys.txt | sed 's/ $*//') | \
$(python -c "import cherrypy; print 'cherrypy',cherrypy.__version__") | \
django $(cut -d$'\t' -f3 data/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" >> ~/.ver_txt

echo -e "\n\n$(tput setab 15)$(tput setaf 16) Das Lab Website Server $(tput sgr 0)" >> ~/.ver_txt
echo -e "$(tput setab 15)$(tput setaf 16) daslab.stanford.edu / 54.149.140.20 $(tput sgr 0)\n" >> ~/.ver_txt
rm temp.txt
echo "Done."


