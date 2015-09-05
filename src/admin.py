from django.contrib import admin
from django.forms import ModelForm, widgets, DateField, DateInput
from django.utils.html import format_html
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# from suit.widgets import AutosizedTextarea
# from suit.widgets import EnclosedInput, SuitDateWidget

import boto.ec2.cloudwatch, boto.ec2.elb

from src.models import *
from src.settings import *
from src.console import *
from src.cron import *


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
    sys_ver_weekly()
    return HttpResponseRedirect('/admin')
admin.site.register_view('sys_stat', view=sys_stat, visible=False)

def backup_stat(request):
    get_backup_stat()
    return HttpResponseRedirect('/admin/backup')
admin.site.register_view('backup_stat', view=backup_stat, visible=False)

def backup_form(request):
    json = get_backup_form()
    return HttpResponse(json, content_type='application/json')

admin.site.register_view('backup_form', view=backup_form, visible=False)

def backup_now(request):
    backup_weekly()
    return backup_stat(request)
admin.site.register_view('backup_now', view=backup_now, visible=False)

def upload_now(request):
    gdrive_weekly()
    return backup_stat(request)
admin.site.register_view('upload_now', view=upload_now, visible=False)

def apache_stat(request):
    json = restyle_apache()
    return HttpResponse(json, content_type='application/json')
admin.site.register_view('apache_stat', view=apache_stat, visible=False)

def apache(request):
    return render_to_response(PATH.HTML_PATH['admin_apache'], {}, context_instance=RequestContext(request))
admin.site.register_view('apache/', view=apache, visible=False)

def aws_stat(request):
    json = aws_stats(request)
    if type(json) is str:
        return HttpResponse(json, content_type='application/json')
    else:
        return json
admin.site.register_view('aws_stat', view=aws_stat, visible=False)

def aws(request):
    conn = boto.ec2.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=False)
    resv = conn.get_only_instances(instance_ids=AWS['EC2_INSTANCE_ID'])
    stat = resv[0].__dict__
    stat1 = {k: stat[k] for k in ('id', 'instance_type', 'private_dns_name', 'public_dns_name', 'vpc_id', 'subnet_id', 'image_id', 'architecture')} 
    resv = conn.get_all_volumes(volume_ids=AWS['EBS_VOLUME_ID'])
    stat = resv[0].__dict__
    stat2 = {k: stat[k] for k in ('id', 'type', 'size', 'zone', 'snapshot_id', 'encrypted')} 

    conn = boto.ec2.elb.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=False)
    resv = conn.get_all_load_balancers(load_balancer_names=AWS['ELB_NAME'])
    stat = resv[0].__dict__
    stat3 = {k: stat[k] for k in ('dns_name', 'vpc_id', 'subnets', 'health_check')} 
    stat3['health_check'] = str(stat3['health_check']).replace('HealthCheck:', '')

    return render_to_response(PATH.HTML_PATH['admin_aws'], {'ec2':stat1, 'ebs':stat2, 'elb':stat3}, context_instance=RequestContext(request))
admin.site.register_view('aws/', view=aws, visible=False)

def ga(request):
    stats = ga_stats()
    stats['client_id'] = GA['CLIENT_ID']
    return render_to_response(PATH.HTML_PATH['admin_ga'], stats, context_instance=RequestContext(request))
admin.site.register_view('ga/', view=ga, visible=False)

def git(request):
    git_stats()
    return render_to_response(PATH.HTML_PATH['admin_git'], {}, context_instance=RequestContext(request))
admin.site.register_view('git/', view=git, visible=False)

# def git_inspector(request):
#     return render_to_response('%s/data/stat_git.html' % MEDIA_ROOT, {}, context_instance=RequestContext(request))
# admin.site.register_view('git_inspector/', view=git_inspector, visible=False)


def backup(request):
    flag = 0
    if request.method == 'POST':
        set_backup_form(request)
        flag = 1

    f = open('%s/config/cron.conf' % MEDIA_ROOT, 'r')
    lines = f.readlines()
    f.close()

    index =  [i for i, line in enumerate(lines) if 'KEEP_BACKUP' in line][0]
    keep = int(lines[index].split(':')[1])
    return render_to_response(PATH.HTML_PATH['admin_backup'], {'form':BackupForm(), 'flag':flag, 'keep':keep, 'email':EMAIL_HOST_USER}, context_instance=RequestContext(request))
admin.site.register_view('backup/', view=backup, visible=False)

def dir(request):
    return render_to_response(PATH.HTML_PATH['admin_dir'], {}, context_instance=RequestContext(request))
admin.site.register_view('dir/', view=dir, visible=False)

def doc(request):
    return render_to_response(PATH.HTML_PATH['admin_doc'], {}, context_instance=RequestContext(request))
admin.site.register_view('doc/', view=doc, visible=False)


def export(request):
    if request.method == 'POST':
        return export_citation(request)
    else:
        return render_to_response(PATH.HTML_PATH['admin_export'], {'form':ExportForm()}, context_instance=RequestContext(request))
admin.site.register_view('export/', view=export, visible=False)


def gcal(request):
    json = get_cal()
    return HttpResponse(json, content_type='application/json')
admin.site.register_view('gcal/', view=gcal, visible=False)


