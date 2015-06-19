from django.contrib import admin
from django.forms import ModelForm, widgets
from django.utils.html import format_html
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
# from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# from suit.widgets import AutosizedTextarea
from suit.widgets import EnclosedInput, SuitDateWidget

from src.models import *
from src.settings import PATH

import subprocess
import sys


UserAdmin.list_display = ('username', 'email', 'last_login', 'is_active', 'is_staff', 'is_superuser')
UserAdmin.ordering = ('-is_superuser', '-is_staff', 'username')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class NewsForm(ModelForm):
    class Meta:
        widgets = {
            'date': SuitDateWidget,
            'content': widgets.Textarea(attrs={'style':'width: 90%','rows':'6' }),
            'link': widgets.TextInput(attrs={'style':'width: 90%' }),
            # 'link': EnclosedInput(prepend='icon-user', attrs={'style':'width: 90%' }),
            'video': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class NewsAdmin(admin.ModelAdmin):
    list_display = ('date', 'content', 'link',)
    ordering = ('-date',)
    form = NewsForm
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<i class="icon-comment"></i> Contents'), {'fields': ['date', 'content', ('image', 'image_tag')]}),
        (format_html('<i class="icon-share"></i> Links'), {'fields': ['link', 'video']}),
    ]
admin.site.register(News, NewsAdmin)


class MemberForm(ModelForm):
    class Meta:
        widgets = {
            'role': widgets.TextInput(attrs={'style':'width: 90%' }),
            'more_info': widgets.TextInput(attrs={'style':'width: 90%' }),
            'description': widgets.TextInput(attrs={'style':'width: 90%' }),
            'department': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class MemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'year', 'joint_lab', 'affiliation',)
    ordering = ('alumni', 'last_name', 'role',)
    form = MemberForm
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<i class="icon-user"></i> Personal Information'), {'fields': [('first_name', 'last_name'), 'role', ('image', 'image_tag'), 'description', 'more_info']}),
        (format_html('<i class="icon-home"></i> Affiliation'), {'fields': ['department', ('joint_lab', 'joint_link')]}),
        (format_html('<i class="icon-road"></i> Alumni Information'), {'fields': ['alumni', ('start_year', 'finish_year')]}),
    ]
admin.site.register(Member, MemberAdmin)


class PublicationForm(ModelForm):
    class Meta:
        widgets = {
            'display_date': SuitDateWidget,
            'authors': widgets.Textarea(attrs={'style':'width: 90%','rows':'4' }),
            'title': widgets.Textarea(attrs={'style':'width: 90%','rows':'4' }),
            'journal': widgets.TextInput(attrs={'style':'width: 90%' }),
            'link': widgets.TextInput(attrs={'style':'width: 90%' }),
            'extra_link': widgets.TextInput(attrs={'style':'width: 90%' }),
            'extra_link_2': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('year', 'journal', 'authors', 'title', 'link',)
    ordering = ('-display_date',)
    form = PublicationForm
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<i class="icon-book"></i> Citation'), {'fields': ['title', ('year', 'display_date'), 'authors', 'journal', ('volume', 'issue'), ('begin_page', 'end_page')]}),
        (format_html('<i class="icon-th-large"></i> Media'), {'fields': ['pdf', 'preprint', 'feature', ('image', 'image_tag')]}),
        (format_html('<i class="icon-share"></i> Links'), {'fields': ['link', 'extra_field', 'extra_link', 'extra_field_2', 'extra_link_2', 'extra_field_3', 'extra_file']}),
    ]
admin.site.register(Publication, PublicationAdmin)


############################################################################################################################################

class FlashSlideForm(ModelForm):
    class Meta:
        widgets = {
            'date': SuitDateWidget,
            'link': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class FlashSlideAdmin(admin.ModelAdmin):
    list_display = ('date', 'link',)
    ordering = ('-date',)
    form = FlashSlideForm

    fieldsets = [
        (format_html('<i class="icon-share"></i> Links'), {'fields': ['date', 'link']}),
    ]
admin.site.register(FlashSlide, FlashSlideAdmin)


class RotationStudentForm(ModelForm):
    class Meta:
        widgets = {
            'date': SuitDateWidget,
            'title': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class RotationStudentAdmin(admin.ModelAdmin):
    list_display = ('date', 'full_name', 'title',)
    ordering = ('-date',)
    form = RotationStudentForm

    fieldsets = [
        (format_html('<i class="icon-user"></i> Personal Information'), {'fields': ['date', 'full_name', 'title']}),
        (format_html('<i class="icon-share"></i> Links'), {'fields': ['ppt', 'data']}),
    ]
admin.site.register(RotationStudent, RotationStudentAdmin)


class EternaYoutubeForm(ModelForm):
    class Meta:
        widgets = {
            'date': SuitDateWidget,
            'link': widgets.TextInput(attrs={'style':'width: 90%' }),
            'title': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class EternaYoutubeAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title', 'link',)
    ordering = ('-date',)
    form = EternaYoutubeForm

    fieldsets = [
        (format_html('<i class="icon-share"></i> Links'), {'fields': ['date', 'presenter', 'title', 'link']}),
    ]
admin.site.register(EternaYoutube, EternaYoutubeAdmin)


class PresentationForm(ModelForm):
    class Meta:
        widgets = {
            'date': SuitDateWidget,
            'link': widgets.TextInput(attrs={'style':'width: 90%' }),
            'title': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class PresentationAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title',)
    ordering = ('-date',)
    form = PresentationForm

    fieldsets = [
        (format_html('<i class="icon-share"></i> Links'), {'fields': ['date', 'presenter', 'title', 'ppt', 'link']}),
    ]
admin.site.register(Presentation, PresentationAdmin)


############################################################################################################################################

def sys_stat(request):
    cpu = subprocess.Popen("uptime | sed 's/.*: //g' | sed 's/,/ \//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

    ver = subprocess.Popen('uname -r | sed %s' % "'s/[a-z\-]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += '%s.%s.%s\t' % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    ver += subprocess.Popen('python -c "import django, suit, filer, adminplus; print %s"' % "django.__version__, '\t', suit.VERSION, '\t', filer.__version__, '\t', adminplus.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

    ver += subprocess.Popen('ls %s' % os.path.join(MEDIA_ROOT, 'media/js/jquery-*.min.js'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].replace(os.path.join(MEDIA_ROOT, 'media/js/jquery-'), '').replace('.min.js', '').strip() + '\t'
    ver += subprocess.Popen('ls %s' % os.path.join(MEDIA_ROOT, 'media/suit/js/jquery-*.min.js'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].replace(os.path.join(MEDIA_ROOT, 'media/suit/js/jquery-'), '').replace('.min.js', '').strip() + '\t'
    f = open(os.path.join(MEDIA_ROOT, 'media/js/bootstrap.min.js'))
    f.readline()
    ver_bootstrap = f.readline()
    ver += ver_bootstrap[ver_bootstrap.find('v')+1: ver_bootstrap.find('(')].strip() + '\t'
    f.close()
    f = open(os.path.join(MEDIA_ROOT, 'media/suit/bootstrap/css/bootstrap.min.css'))
    f.readline()
    ver_bootstrap = f.readline()
    ver += ver_bootstrap[ver_bootstrap.find('v')+1: ].strip() + '\t'
    f.close()

    ver += subprocess.Popen('mysql --version | sed %s | sed %s' % ("'s/,.*//g'", "'s/.*Distrib //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen('apachectl -v | head -1 | sed %s | sed %s' % ("'s/.*\///g'", "'s/[a-zA-Z \(\)]//g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += 'N/A\t'

    ver += subprocess.Popen('ssh -V 2> temp.txt && sed %s temp.txt | sed %s | sed %s | sed %s' % ("'s/^OpenSSH\_//g'", "'s/U.*//'", "'s/,.*//g'", "'s/[a-z]/./g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen("git --version | sed 's/.*version //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

    ver += subprocess.Popen('python -c "import virtualenv, pip; print %s"' % "pip.__version__, '\t', virtualenv.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    
    disk_sp = subprocess.Popen('df -h | head -2 | tail -1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].split()
    ver += '%s / %s' % (disk_sp[3], disk_sp[2]) + '\t'
    if subprocess.Popen('uname', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() == 'Darwin':
        mem_str = subprocess.Popen('top -l 1 | head -n 10 | grep PhysMem', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
        mem_avail = mem_str[mem_str.find(',')+1:mem_str.find('unused')].strip()
        mem_used = mem_str[mem_str.find(':')+1:mem_str.find('used')].strip()
    else:
        mem_str = subprocess.Popen('free -h', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split('\n')
        mem_avail = [x for x in mem_str[2].split(' ') if x][-1]
        mem_used = [x for x in mem_str[2].split(' ') if x][-2]
    ver += '%s / %s' % (mem_avail, mem_used) + '\t'
    ver += subprocess.Popen('du -h %s' % os.path.join(MEDIA_ROOT, '../mysql_dump.gz'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
    ver += cpu + '\t'

    ver += str(int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/news_img/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1) + '\t'
    ver += subprocess.Popen('du -h %s' % os.path.join(MEDIA_ROOT, 'data/news_img/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
    ver += str(int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/ppl_img/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1) + '\t'
    ver += subprocess.Popen('du -h %s' % os.path.join(MEDIA_ROOT, 'data/ppl_img/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'

    ver += str(int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/pub_pdf/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1 + int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/pub_img/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1 + int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/pub_data/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1) + '\t'
    ver += subprocess.Popen('du -h --total %s %s %s | tail -1' % (os.path.join(MEDIA_ROOT, 'data/pub_pdf/'), os.path.join(MEDIA_ROOT, 'data/pub_img/'), os.path.join(MEDIA_ROOT, 'data/pub_data/')), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
    
    ver += str(int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/rot_ppt/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1 + int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/rot_data/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1) + '\t'
    ver += subprocess.Popen('du -h --total %s %s' % (os.path.join(MEDIA_ROOT, 'data/rot_ppt/'), os.path.join(MEDIA_ROOT, 'data/rot_data/')), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
    
    ver += str(int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_ROOT, 'data/spe_ppt/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1) + '\t'
    ver += subprocess.Popen('du -h %s' % os.path.join(MEDIA_ROOT, 'data/spe_ppt/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'


    f = open(os.path.join(MEDIA_ROOT, 'data/sys_ver.txt'), 'w')
    f.write(ver)
    f.close()
    subprocess.Popen('rm temp.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return HttpResponse('<html><body onLoad="window.close()"></body></html>')
admin.site.register_view('sys_stat', view=sys_stat, visible=False)


def apache(request):
    return render_to_response(PATH.HTML_PATH['admin_apache'], {}, context_instance=RequestContext(request))
admin.site.register_view('apache', view=apache, visible=False)

def doc(request):
    return render_to_response(PATH.HTML_PATH['admin_doc'], {}, context_instance=RequestContext(request))
admin.site.register_view('doc', view=doc, visible=False)


