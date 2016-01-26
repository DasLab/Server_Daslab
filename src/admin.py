from django.contrib import admin
from django.forms import ModelForm, widgets, DateField, DateInput
from django.utils.html import format_html
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.management import call_command

# from suit.widgets import AutosizedTextarea
# from suit.widgets import EnclosedInput, SuitDateWidget

from datetime import datetime
import os
import time

from src.console import *
from src.dash import *
from src.env import error400
from src.models import *
from src.settings import *


UserAdmin.list_display = ('username', 'email', 'last_login', 'is_active', 'is_staff', 'is_superuser')
UserAdmin.ordering = ('-is_superuser', '-is_staff', 'username')
# admin.site.unregister(User)
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
    list_display = ('full_name', 'sunet_id', 'year', 'joint_lab', 'affiliation',)
    ordering = ('is_alumni', 'last_name', 'role',)
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-user"></span>&nbsp;Personal Information'), {'fields': [('first_name', 'last_name'), 'role', ('image', 'image_tag'), 'description', 'more_info']}),
        (format_html('<span class="glyphicon glyphicon-home"></span>&nbsp;Affiliation'), {'fields': ['department', ('joint_lab', 'joint_link')]}),
        (format_html('<span class="glyphicon glyphicon-earphone"></span>&nbsp;Contact'), {'fields': [('email', 'bday'), ('sunet_id', 'phone')]}),
        (format_html('<span class="glyphicon glyphicon-road"></span>&nbsp;Alumni Information'), {'fields': [('is_alumni', 'is_visible'), ('start_year', 'finish_year')]}),
    ]
admin.site.register(Member, MemberAdmin)

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('year', 'journal', 'authors', 'title', 'link',)
    ordering = ('-display_date',)
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-book"></span>&nbsp;Citation'), {'fields': ['title', ('year', 'display_date'), 'authors', 'journal', ('volume', 'issue'), ('begin_page', 'end_page')]}),
        (format_html('<span class="glyphicon glyphicon-th-large"></span>&nbsp;Media'), {'fields': ['pdf', 'is_preprint', 'is_visible', 'is_feature', ('image', 'image_tag')]}),
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

class JournalClubAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title', 'link',)
    ordering = ('-date',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['date', 'presenter', 'link', 'title', ('authors', 'year'), 'citation']}),
    ]
admin.site.register(JournalClub, JournalClubAdmin)

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

class SlackMessageAdmin(admin.ModelAdmin):
    list_display = ('date', 'receiver', 'message')
    ordering = ('-date',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-comment"></span>&nbsp;Contents'), {'fields': ['date', 'receiver', 'content', 'attachment']}),
    ]
admin.site.register(SlackMessage, SlackMessageAdmin)


############################################################################################################################################

def sys_stat(request):
    call_command('versions', '1')
    return HttpResponseRedirect('/admin/')

def backup_stat(request):
    get_backup_stat()
    return HttpResponseRedirect('/admin/backup/')

def backup_form(request):
    return HttpResponse(simplejson.dumps(get_backup_form(), sort_keys=True, indent=' ' * 4), content_type='application/json')

def backup_now(request):
    call_command('backup')
    return backup_stat(request)

def upload_now(request):
    call_command('gdrive')
    return backup_stat(request)


def apache_stat(request):
    return HttpResponse(restyle_apache(), content_type='application/json')

def apache(request):
    return render_to_response(PATH.HTML_PATH['admin_apache'], {'host_name':env('SSL_HOST')}, context_instance=RequestContext(request))


def aws(request):
    return render_to_response(PATH.HTML_PATH['admin_aws'], {'timezone':TIME_ZONE}, context_instance=RequestContext(request))

def aws_stat(request):
    json = aws_stats(request)
    if isinstance(json, HttpResponse): return json
    return HttpResponse(json, content_type='application/json')

def ga(request):
    return render_to_response(PATH.HTML_PATH['admin_ga'], {'ga_url':GA['LINK_URL']}, context_instance=RequestContext(request))

def ga_stat(request):
    json = ga_stats(request)
    if isinstance(json, HttpResponse): return json
    return HttpResponse(json, content_type='application/json')

def git(request):
    return render_to_response(PATH.HTML_PATH['admin_git'], {'timezone':TIME_ZONE, 'git_repo':GIT['REPOSITORY']}, context_instance=RequestContext(request))

def git_stat(request):
    json = git_stats(request)
    if isinstance(json, HttpResponse): return json
    return HttpResponse(json, content_type='application/json')

def ssl_dash(request):
    return HttpResponse(dash_ssl(request), content_type='application/json')

def group_dash(request):
    json = simplejson.dumps({'admin':GROUP.ADMIN, 'group':GROUP.GROUP, 'alumni':GROUP.ALUMNI, 'roton':GROUP.ROTON, 'other':GROUP.OTHER}, sort_keys=True, indent=' ' * 4)
    return HttpResponse(json, content_type='application/json')

def dash_dash(request):
    t_aws = format_dash_ts('aws/init.pickle', BOT['CACHE']['INTERVAL_15'])
    t_ga = format_dash_ts('ga/init.pickle', BOT['CACHE']['INTERVAL_15'])
    t_git = format_dash_ts('git/init.pickle', BOT['CACHE']['INTERVAL_30'])
    t_slack = format_dash_ts('slack/users.pickle', BOT['CACHE']['INTERVAL_30'])
    t_dropbox = format_dash_ts('dropbox/sizes.pickle', BOT['CACHE']['INTERVAL_30'])
    t_cal = format_dash_ts('calendar.pickle', BOT['CACHE']['INTERVAL_30'])
    t_sch = format_dash_ts('schedule.pickle', BOT['CACHE']['INTERVAL_30'])
    t_duty = format_dash_ts('duty.pickle', BOT['CACHE']['INTERVAL_30'])
    json = {'t_aws':t_aws, 't_ga':t_ga, 't_git':t_git, 't_slack':t_slack, 't_dropbox':t_dropbox, 't_cal':t_cal, 't_sch':t_sch, 't_duty':t_duty}
    return HttpResponse(simplejson.dumps(json, sort_keys=True, indent=' ' * 4), content_type='application/json')

def dash_stat(request):
    if request.META.has_key('QUERY_STRING'):
        flag = request.META['QUERY_STRING'].replace('int=', '')
        if flag in ('3', '15', '30'):
            call_command('cache', flag)
        else:
            return error400(request, True)
    else:
        return error400(request, True)
    return HttpResponseRedirect('/admin/')


def backup(request):
    flag = -1
    if request.method == 'POST':
        flag = set_backup_form(request)

    form = BackupForm(initial=get_backup_form())
    return render_to_response(PATH.HTML_PATH['admin_backup'], {'form':form, 'flag':flag, 'email':EMAIL_HOST_USER}, context_instance=RequestContext(request))

def bot(request):
    flag = -1
    if request.method == 'POST':
        flag = set_bot_form(request)

    form = BotSettingForm(initial=get_bot_form())
    return render_to_response(PATH.HTML_PATH['admin_bot'], {'form':form, 'flag':flag, 'BOT':BOT}, context_instance=RequestContext(request))

def dir(request):
    return render_to_response(PATH.HTML_PATH['admin_dir'], {}, context_instance=RequestContext(request))

def slack(request):
    return render_to_response(PATH.HTML_PATH['admin_slack'], {}, context_instance=RequestContext(request))

def export(request):
    if request.method == 'POST':
        return export_citation(request)
    else:
        return render_to_response(PATH.HTML_PATH['admin_export'], {'form':ExportForm()}, context_instance=RequestContext(request))


def doc(request):
    return render_to_response(PATH.HTML_PATH['admin_doc'], {}, context_instance=RequestContext(request))


def get_ver(request):
    lines = open('%s/cache/stat_sys.txt' % MEDIA_ROOT, 'r').readlines()
    lines = ''.join(lines)
    return HttpResponse(lines, content_type='text/plain')

def get_backup(request):
    lines = open('%s/cache/stat_backup.txt' % MEDIA_ROOT, 'r').readlines()
    lines = ''.join(lines)
    return HttpResponse(lines, content_type='text/plain')


admin.site.register_view('backup/', view=backup, visible=False)
admin.site.register_view('backup_stat/', view=backup_stat, visible=False)
admin.site.register_view('backup_form/', view=backup_form, visible=False)
admin.site.register_view('backup_now/', view=backup_now, visible=False)
admin.site.register_view('upload_now/', view=upload_now, visible=False)

admin.site.register_view('apache_stat/', view=apache_stat, visible=False)
admin.site.register_view('apache/', view=apache, visible=False)

admin.site.register_view('aws/', view=aws, visible=False)
admin.site.register_view('aws_stat/', view=aws_stat, visible=False)

admin.site.register_view('ga/', view=ga, visible=False)
admin.site.register_view('ga_stat/', view=ga_stat, visible=False)

admin.site.register_view('git/', view=git, visible=False)
admin.site.register_view('git_stat/', view=git_stat, visible=False)

admin.site.register_view('sys_stat/', view=sys_stat, visible=False)
admin.site.register_view('ssl_dash/', view=ssl_dash, visible=False)
admin.site.register_view('group_dash/', view=group_dash, visible=False)
admin.site.register_view('dash_dash/', view=dash_dash, visible=False)
admin.site.register_view('dash_stat/', view=dash_stat, visible=False)

admin.site.register_view('dir/', view=dir, visible=False)
admin.site.register_view('bot/', view=bot, visible=False)
admin.site.register_view('slack/', view=slack, visible=False)
admin.site.register_view('export/', view=export, visible=False)

admin.site.register_view('doc/', view=doc, visible=False)

admin.site.register_view('get_ver/', view=get_ver, visible=False)
admin.site.register_view('get_backup/', view=get_backup, visible=False)

