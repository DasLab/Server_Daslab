from django.contrib import admin
from django.forms import ModelForm, widgets, DateField, DateInput
from django.utils.html import format_html
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
# from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# from suit.widgets import AutosizedTextarea
# from suit.widgets import EnclosedInput, SuitDateWidget

from src.models import *
from src.settings import PATH, env
from src.console import *


UserAdmin.list_display = ('username', 'email', 'last_login', 'is_active', 'is_staff', 'is_superuser')
UserAdmin.ordering = ('-is_superuser', '-is_staff', 'username')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('date', 'content', 'link',)
    ordering = ('-date',)
    # form = NewsForm
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-comment"></span>&nbsp;Contents'), {'fields': ['date', 'content', ('image', 'image_tag')]}),
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['link', 'video']}),
    ]
admin.site.register(News, NewsAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'year', 'joint_lab', 'affiliation',)
    ordering = ('alumni', 'last_name', 'role',)
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-user"></span>&nbsp;Personal Information'), {'fields': [('first_name', 'last_name'), 'role', ('image', 'image_tag'), 'description', 'more_info']}),
        (format_html('<span class="glyphicon glyphicon-home"></span>&nbsp;Affiliation'), {'fields': ['department', ('joint_lab', 'joint_link')]}),
        (format_html('<span class="glyphicon glyphicon-road"></span>&nbsp;Alumni Information'), {'fields': ['alumni', ('start_year', 'finish_year')]}),
    ]
admin.site.register(Member, MemberAdmin)

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('year', 'journal', 'authors', 'title', 'link',)
    ordering = ('-display_date',)
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-book"></span>&nbsp;Citation'), {'fields': ['title', ('year', 'display_date'), 'authors', 'journal', ('volume', 'issue'), ('begin_page', 'end_page')]}),
        (format_html('<span class="glyphicon glyphicon-th-large"></span>&nbsp;Media'), {'fields': ['pdf', 'preprint', 'feature', ('image', 'image_tag')]}),
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['link', 'extra_field', 'extra_link', 'extra_field_2', 'extra_link_2', 'extra_field_3', 'extra_file']}),
    ]
admin.site.register(Publication, PublicationAdmin)


############################################################################################################################################

class FlashSlideAdmin(admin.ModelAdmin):
    list_display = ('date', 'link',)
    ordering = ('-date',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['date', 'link']}),
    ]
admin.site.register(FlashSlide, FlashSlideAdmin)

class RotationStudentAdmin(admin.ModelAdmin):
    list_display = ('date', 'full_name', 'title',)
    ordering = ('-date',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-user"></span>&nbsp;Personal Information'), {'fields': ['date', 'full_name', 'title']}),
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['ppt', 'data']}),
    ]
admin.site.register(RotationStudent, RotationStudentAdmin)

class EternaYoutubeAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title', 'link',)
    ordering = ('-date',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['date', 'presenter', 'title', 'link']}),
    ]
admin.site.register(EternaYoutube, EternaYoutubeAdmin)

class PresentationAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title',)
    ordering = ('-date',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['date', 'presenter', 'title', 'ppt', 'link']}),
    ]
admin.site.register(Presentation, PresentationAdmin)


############################################################################################################################################

def sys_stat(request):
    get_sys_stat()
    return HttpResponse('<html><body onLoad="window.close()"></body></html>')
admin.site.register_view('sys_stat', view=sys_stat, visible=False)

def apache(request):
    return render_to_response(PATH.HTML_PATH['admin_apache'], {'cred':'%s:%s' % (env('APACHE_USER'), env('APACHE_PASSWORD'))}, context_instance=RequestContext(request))
admin.site.register_view('apache/', view=apache, visible=False)

def dir(request):
    return render_to_response(PATH.HTML_PATH['admin_dir'], {}, context_instance=RequestContext(request))
admin.site.register_view('dir/', view=dir, visible=False)

def doc(request):
    return render_to_response(PATH.HTML_PATH['admin_doc'], {}, context_instance=RequestContext(request))
admin.site.register_view('doc/', view=doc, visible=False)


