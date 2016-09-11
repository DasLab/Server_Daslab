from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.management import call_command


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
        (format_html('<span class="glyphicon glyphicon-comment"></span>&nbsp;Contents'), {'fields': ['date', 'content', 'is_visible', ('image', 'image_tag')]}),
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

class DefensePosterAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title',)
    ordering = ('-date',)
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-share"></span>&nbsp;Links'), {'fields': ['date', 'presenter', 'title', 'image', 'image_tag']}),
    ]
admin.site.register(DefensePoster, DefensePosterAdmin)

class SlackMessageAdmin(admin.ModelAdmin):
    list_display = ('date', 'receiver', 'message')
    ordering = ('-date',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-comment"></span>&nbsp;Contents'), {'fields': ['date', 'receiver', 'content', 'attachment']}),
    ]
admin.site.register(SlackMessage, SlackMessageAdmin)


############################################################################################################################################

def backup_form(request):
    return HttpResponse(simplejson.dumps(get_backup_form(), sort_keys=True, indent=' ' * 4), content_type='application/json')

def admin_cmd(request, keyword):
    keyword = 'gdrive' if keyword.strip('/') == 'upload' else 'backup'
    call_command(keyword)
    return refresh_stat(request, 'backup')


def apache(request):
    return render(request, PATH.HTML_PATH['admin_apache'], {'host_name': env('SSL_HOST')})

def aws(request):
    return render(request, PATH.HTML_PATH['admin_aws'], {'timezone': TIME_ZONE})

def ga(request):
    return render(request, PATH.HTML_PATH['admin_ga'], {'ga_url': GA['LINK_URL']})

def git(request):
    return render(request, PATH.HTML_PATH['admin_git'], {'timezone': TIME_ZONE, 'git_repo': GIT['REPOSITORY']})


def backup(request):
    flag = -1
    if request.method == 'POST':
        flag = set_backup_form(request)

    form = BackupForm(initial=get_backup_form())
    return render(request, PATH.HTML_PATH['admin_backup'], {'form': form, 'flag': flag, 'email': EMAIL_HOST_USER})

def bot(request):
    flag = -1
    if request.method == 'POST':
        flag = set_bot_form(request)

    form = BotSettingForm(initial=get_bot_form())
    return render(request, PATH.HTML_PATH['admin_bot'], {'form': form, 'flag': flag, 'BOT': BOT})

def dir(request):
    return render(request, PATH.HTML_PATH['admin_dir'], {})

def export(request):
    if request.method == 'POST':
        return export_citation(request)
    else:
        return render(request, PATH.HTML_PATH['admin_export'], {'form': ExportForm()})


def man(request):
    return render(request, PATH.HTML_PATH['admin_man'], {})

def ref(request):
    return render(request, PATH.HTML_PATH['admin_ref'], {})

def key(request):
    return render(request, PATH.HTML_PATH['admin_secret'], {})


def get_stat(request, keyword):
    if keyword == "pem":
        return HttpResponse(''.join(open('%s/config/amazon.pem' % MEDIA_ROOT).readlines()), content_type='application/x-pem-file')
    elif keyword == "key":
        (gmail, db) = (env.email_url(), env.db())
        json = {'mysql': {'user': db['USER'], 'password': db['PASSWORD']}, 'apache': {'user': env('APACHE_USER'), 'password': env('APACHE_PASSWORD')}, 'django': {'user': env('DJANGO_USER'), 'password': env('DJANGO_PASSWORD')}, 'gmail': {'user': gmail['EMAIL_HOST_USER'], 'password': gmail['EMAIL_HOST_PASSWORD']}, 'vendor': {'user': gmail['EMAIL_HOST_USER'], 'password': GIT['PASSWORD']}}
    else:
        json = simplejson.load(open('%s/cache/stat_%s.json' % (MEDIA_ROOT, keyword.strip('/')), 'r'))
    return HttpResponse(simplejson.dumps(json, sort_keys=True, indent=' ' * 4), content_type='application/json')

def refresh_stat(request, keyword):
    keyword = keyword.strip('/')
    if keyword == 'sys':
        call_command('versions', '1')
        return HttpResponseRedirect('/admin/')
    elif keyword == 'backup':
        get_backup_stat()
        return HttpResponseRedirect('/admin/backup/')
    elif keyword == 'dash':
        if 'QUERY_STRING' in request.META:
            flag = request.META['QUERY_STRING'].replace('int=', '')
            if flag in ('3', '15', '30'):
                call_command('cache', flag)
            else:
                return error400(request)
        else:
            return error400(request)
        return HttpResponseRedirect('/admin/')

def get_dash(request, keyword):
    if keyword == 'apache':
        json = restyle_apache()
    elif keyword == 'aws':
        json = aws_stats(request)
    elif keyword == 'ga':
        json = ga_stats(request)
    elif keyword == 'git':
        json = git_stats(request)
    elif keyword == 'group':
        json = simplejson.dumps({'admin': GROUP.ADMIN, 'group': GROUP.GROUP, 'alumni': GROUP.ALUMNI, 'roton': GROUP.ROTON, 'other': GROUP.OTHER}, sort_keys=True, indent=' ' * 4)
    elif keyword == 'dash':
        t_aws = format_dash_ts('aws/init.json', BOT['CACHE']['INTERVAL_15'])
        t_ga = format_dash_ts('ga/init.json', BOT['CACHE']['INTERVAL_15'])
        t_git = format_dash_ts('git/init.json', BOT['CACHE']['INTERVAL_30'])
        t_slack = format_dash_ts('slack/users.json', BOT['CACHE']['INTERVAL_30'])
        t_dropbox = format_dash_ts('dropbox/sizes.json', BOT['CACHE']['INTERVAL_30'])
        t_cal = format_dash_ts('calendar.json', BOT['CACHE']['INTERVAL_30'])
        t_sch = format_dash_ts('schedule.json', BOT['CACHE']['INTERVAL_30'])
        t_duty = format_dash_ts('duty.json', BOT['CACHE']['INTERVAL_30'])
        json = simplejson.dumps({'t_aws': t_aws, 't_ga': t_ga, 't_git': t_git, 't_slack': t_slack, 't_dropbox': t_dropbox, 't_cal': t_cal, 't_sch': t_sch, 't_duty': t_duty}, sort_keys=True, indent=' ' * 4)

    if isinstance(json, HttpResponse): return json
    return HttpResponse(json, content_type='application/json')


admin.site.register_view('backup/', view=backup, visible=False)
admin.site.register_view('backup/form/', view=backup_form, visible=False)
admin.site.register_view(r'cmd/(upload|backup)/?$', view=admin_cmd, visible=False)

admin.site.register_view('apache/', view=apache, visible=False)
admin.site.register_view('aws/', view=aws, visible=False)
admin.site.register_view('ga/', view=ga, visible=False)
admin.site.register_view('git/', view=git, visible=False)

admin.site.register_view('dir/', view=dir, visible=False)
admin.site.register_view('bot/', view=bot, visible=False)
admin.site.register_view('export/', view=export, visible=False)

admin.site.register_view('man/', view=man, visible=False)
admin.site.register_view('ref/', view=ref, visible=False)
admin.site.register_view('key/', view=key, visible=False)

admin.site.register_view(r'dash/(apache|aws|ga|git|group|dash)/?$', view=get_dash, visible=False)
admin.site.register_view(r'stat/(ver|sys|backup|pem|key)/?$', view=get_stat, visible=False)
admin.site.register_view(r'stat/(sys|backup|dash)/refresh/?$', view=refresh_stat, visible=False)
