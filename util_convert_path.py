import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append(os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings") 
application = get_wsgi_application()

from src.settings import *
from src.models import *


dev = '/MATLAB_Code/Daslab_server/data/'
release = '/home/ubuntu/Files/'

if len(sys.argv) != 2:
	print('Usage:')
	print('    %s <flag>' % sys.argv[0])
	print('    <flag> is chosen from "dev" or "release", indicating the target.')
	exit()

target = sys.argv[1]
if target == 'dev':
	old = release
	new = dev
elif target == 'release':
	old = dev
	new = release
else:
	print('Usage:')
	print('    %s <flag>' % sys.argv[0])
	print('    <flag> is chosen from "dev" or "release", indicating the target.')
	exit()


print "Converting database path to \033[94m%s\033[0m..." % target

entries = News.objects.all()
for e in entries:
	if e.image:
		e.image = e.image.url.replace(old, new)
		e.save()
print "\033[92mSUCCESS\033[0m: ", len(entries), "of News image converted.\033[0m"

entries = Member.objects.all()
for e in entries:
	if e.image:
		e.image = e.image.url.replace(old, new)
		e.save()
print "\033[92mSUCCESS\033[0m: ", len(entries), "of Member image converted.\033[0m"

entries = Publication.objects.all()
for e in entries:
	if e.pdf:
		e.pdf = e.pdf.url.replace(old, new)
		e.save()
	if e.extra_file:
		e.extra_file = e.extra_file.url.replace(old, new)
		e.save()
	if e.image:
		e.image = e.image.url.replace(old, new)
		e.save()
print "\033[92mSUCCESS\033[0m: ", len(entries), "of Publication pdf, extra_file, image converted.\033[0m"

entries = RotationStudent.objects.all()
for e in entries:
	if e.ppt:
		e.ppt = e.ppt.url.replace(old, new)
		e.save()
	if e.data:
		e.data = e.data.url.replace(old, new)
		e.save()
print "\033[92mSUCCESS\033[0m: ", len(entries), "of RotationStudent ppt, data converted.\033[0m"

entries = Presentation.objects.all()
for e in entries:
	if e.ppt:
		e.ppt = e.ppt.url.replace(old, new)
		e.save()
print "\033[92mSUCCESS\033[0m: ", len(entries), "of Presentation ppt converted.\033[0m"
print "All done!"

