from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from django.contrib import messages
# from django.db import IntegrityError
# from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.shortcuts import render, render_to_response

from filemanager import FileManager

from src.console import *
from src.dash import *
from src.models import *
from src.settings import *

import re
import traceback

colors = ('brown', 'dark-red', 'danger', 'orange', 'warning', 'green', 'success', 'light-blue', 'info', 'primary', 'dark-blue', 'violet')


def index(request):
    return render_to_response(PATH.HTML_PATH['index'], {}, context_instance=RequestContext(request))
def research(request):
    return render_to_response(PATH.HTML_PATH['research'], {}, context_instance=RequestContext(request))
def resources(request):
    return render_to_response(PATH.HTML_PATH['resources'], {}, context_instance=RequestContext(request))
def contact(request):
    return render_to_response(PATH.HTML_PATH['contact'], {}, context_instance=RequestContext(request))

def news(request):
    news_list = News.objects.order_by('-date')
    for news in news_list:
        if news.image:
            news.image_link = os.path.basename(news.image.name)
    return render_to_response(PATH.HTML_PATH['news'], {'news_list':news_list}, context_instance=RequestContext(request))

def people(request):
    member = Member.objects.filter(is_alumni=0, is_visible=1).order_by('last_name', 'first_name')
    almuni = Member.objects.filter(is_alumni=1, is_visible=1).order_by('finish_year', 'start_year')
    for ppl in member:
        if ppl.image:
            ppl.image_link = os.path.basename(ppl.image.name)
    return render_to_response(PATH.HTML_PATH['people'], {'current_member':member, 'past_member':almuni}, context_instance=RequestContext(request))

def publications(request):
    pub_list = Publication.objects.filter(is_visible=1).order_by('-display_date')
    for i, pub in enumerate(pub_list):
        if pub.image:
            pub.image_link = os.path.basename(pub.image.name)
        if pub.pdf:
            pub.pdf_link = os.path.basename(pub.pdf.name)
        if pub.extra_file:
            pub.file_link = os.path.basename(pub.extra_file.name)
        if i == 0 or pub_list[i-1].year != pub.year:
            pub.year_tag = True
        if pub.year == 2009 and pub_list[i-1].year == 2010:
            pub.previous = True
    return render_to_response(PATH.HTML_PATH['publications'], {'pub_list':pub_list}, context_instance=RequestContext(request))


############################################################################################################################################

# @login_required
def lab_meeting_schedule(request):
    return render_to_response(PATH.HTML_PATH['lab_meeting_schedule'], {}, context_instance=RequestContext(request))

# @login_required
def lab_meeting_flash(request):
    flash_list = FlashSlide.objects.order_by('-date')
    for i, gp in enumerate(flash_list):
        if i == 0 or flash_list[i - 1].date.year != gp.date.year:
            gp.year_start = True
        if i == len(flash_list) - 1 or flash_list[i + 1].date.year != gp.date.year:
            gp.year_end = True
        if i == 0 or flash_list[i - 1].date.month != gp.date.month:
            gp.month_start = True
            gp.label = colors[gp.date.month - 1]
        if i == len(flash_list) - 1 or flash_list[i + 1].date.month != gp.date.month:
            gp.month_end = True 
    return render_to_response(PATH.HTML_PATH['lab_meeting_flash'], {'flash_list':flash_list}, context_instance=RequestContext(request))

# @login_required
def lab_meeting_jc(request):
    jc_list = JournalClub.objects.order_by('-date')
    for i, gp in enumerate(jc_list):
        gp.label = colors[11 - i % 12]
        if i == 0 or jc_list[i - 1].date.year != gp.date.year:
            gp.year_start = True
    return render_to_response(PATH.HTML_PATH['lab_meeting_jc'], {'jc_list':jc_list}, context_instance=RequestContext(request))

# @login_required
def lab_meeting_youtube(request):
    eterna_list = EternaYoutube.objects.order_by('-date')
    for i, gp in enumerate(eterna_list):
        gp.label = colors[11 - i % 12]
        if i == 0 or eterna_list[i - 1].date.year != gp.date.year:
            gp.year_start = True
    return render_to_response(PATH.HTML_PATH['lab_meeting_eterna'], {'eterna_list':eterna_list}, context_instance=RequestContext(request))

# @login_required
def lab_meeting_rotation(request):
    rot_list = RotationStudent.objects.order_by('-date')
    for i, rot in enumerate(rot_list):
        rot.label = colors[11 - i % 12]
        if i == 0 or rot_list[i - 1].date.year != rot.date.year:
            rot.year_start = True
        if rot.ppt:
            rot.ppt_link = os.path.basename(rot.ppt.name)
        if rot.data:
            rot.dat_link = os.path.basename(rot.data.name)
    return render_to_response(PATH.HTML_PATH['lab_meeting_rotation'], {'rot_list':rot_list}, context_instance=RequestContext(request))

# @login_required
def lab_resource_gdocs(request):
    return render_to_response(PATH.HTML_PATH['lab_resource_gdocs'], {}, context_instance=RequestContext(request))
# @login_required
def lab_resource_archive(request):
    arv_list = Presentation.objects.order_by('-date')
    for i, arv in enumerate(arv_list):
        arv.label = colors[11 - i % 12]
        if i == 0 or arv_list[i - 1].date.year != arv.date.year:
            arv.year_start = True
        if arv.ppt:
            arv.ppt_link = os.path.basename(arv.ppt.name).replace('C:\\fakepath\\', '')
    return render_to_response(PATH.HTML_PATH['lab_resource_archive'], {'arv_list':arv_list}, context_instance=RequestContext(request))
# @login_required
def lab_resource_contact(request):
    member = Member.objects.filter(is_alumni=0).exclude(sunet_id=request.user.username).order_by('last_name', 'first_name')
    for i, ppl in enumerate(member):
        ppl.label = colors[11 - i % 12]
        ppl.name = ppl.full_name()
        ppl.photo = ppl.image_tag()
        ppl.title = ppl.affiliation()
        ppl.status = ppl.year()
        if ppl.phone:
            ppl.phone = str(ppl.phone)
            ppl.phone = '(%s) %s-%s' % (ppl.phone[:3], ppl.phone[3:6], ppl.phone[6:])

    almuni = Member.objects.filter(is_alumni=1).order_by('-finish_year', '-start_year')
    for i, ppl in enumerate(almuni):
        ppl.label = colors[11 - i % 12]
        if i == 0 or almuni[i - 1].finish_year != ppl.finish_year:
            ppl.year_start = True
        ppl.name = ppl.full_name()
        ppl.photo = ppl.image_tag()
        ppl.title = ppl.affiliation()
        ppl.status = ppl.year()
        if ppl.phone:
            ppl.phone = str(ppl.phone)
            ppl.phone = '(%s) %s-%s' % (ppl.phone[:3], ppl.phone[3:6], ppl.phone[6:])
    return render_to_response(PATH.HTML_PATH['lab_resource_contact'], {'current_member':member, 'past_member':almuni}, context_instance=RequestContext(request))


# @login_required
def lab_home(request):
    return render_to_response(PATH.HTML_PATH['lab_home'], {}, context_instance=RequestContext(request))
# @login_required
def lab_calendar(request):
    return render_to_response(PATH.HTML_PATH['lab_calendar'], {}, context_instance=RequestContext(request))
# @login_required
def lab_server_aws(request):
    return render_to_response(PATH.HTML_PATH['lab_server_aws'], {}, context_instance=RequestContext(request))
# @login_required
def lab_server_ga(request):
    return render_to_response(PATH.HTML_PATH['lab_server_ga'], {}, context_instance=RequestContext(request))
# @login_required
def lab_service_bot(request):
    return render_to_response(PATH.HTML_PATH['lab_service_bot'], {}, context_instance=RequestContext(request))
# @login_required
def lab_service_git(request):
    return render_to_response(PATH.HTML_PATH['lab_service_git'], {}, context_instance=RequestContext(request))
# @login_required
def lab_service_slack(request):
    return render_to_response(PATH.HTML_PATH['lab_service_slack'], {}, context_instance=RequestContext(request))
# @login_required
def lab_service_dropbox(request):
    return render_to_response(PATH.HTML_PATH['lab_service_dropbox'], {}, context_instance=RequestContext(request))
# @login_required
def lab_misc(request):
    return render_to_response(PATH.HTML_PATH['lab_misc'], {}, context_instance=RequestContext(request))
# @login_required
def lab_error(request):
    return render_to_response(PATH.HTML_PATH['lab_error'], {}, context_instance=RequestContext(request))


def user_login(request):
    if request.user.is_authenticated():
        if request.GET.has_key('next') and 'admin' in request.GET['next']:
            return error403(request)
        return HttpResponseRedirect('/group/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        messages = 'Invalid username and/or password. Please try again.'
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            flag = form.cleaned_data['flag']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if flag == "Admin":
                        return HttpResponseRedirect('/admin/')
                    else:
                        return HttpResponseRedirect('/group/')
                else:
                    messages = 'Inactive/disabled account. Please contact us.'
        return render_to_response(PATH.HTML_PATH['login'], {'form': form, 'messages':messages}, context_instance=RequestContext(request))
    else:
        if request.GET.has_key('next') and 'admin' in request.GET['next']:
            flag = 'Admin'
        else:
            flag = 'Member'
        form = LoginForm(initial={'flag': flag})
        return render_to_response(PATH.HTML_PATH['login'], {'form': form}, context_instance=RequestContext(request))

# @login_required
def user_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password_old = form.cleaned_data['password_old']
            password_new = form.cleaned_data['password_new']
            password_new_rep = form.cleaned_data['password_new_rep']
            if password_new != password_new_rep:
                return render_to_response(PATH.HTML_PATH['password'], {'form': form, 'messages':'New password does not match. Please try again.'}, context_instance=RequestContext(request))
            if password_new == password_old:
                return render_to_response(PATH.HTML_PATH['password'], {'form': form, 'messages':'New password is the same as current. Please try again.'}, context_instance=RequestContext(request))

            user = authenticate(username=username, password=password_old)
            if user is not None:
                u = User.objects.get(username=username)
                u.set_password(password_new)
                u.save()
                logout(request)
                return render_to_response(PATH.HTML_PATH['password'], {'form': form, 'notices':'Password change successful. Please sign in using new credentials.'}, context_instance=RequestContext(request))
        form = PasswordForm(initial={'username': request.user.username})
        return render_to_response(PATH.HTML_PATH['password'], {'form': form, 'messages':'Invalid username and/or current password, or missing new password.<br/>Please try again.'}, context_instance=RequestContext(request))
    else:
        form = PasswordForm(initial={'username': request.user.username})
        return render_to_response(PATH.HTML_PATH['password'], {'form': form}, context_instance=RequestContext(request))

# @login_required
def user_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                bday = form.cleaned_data['bday']
                bday = re.match('[0-9]{1,2}\/[0-9]{1,2}', bday)
                if bday is None: raise ValueError
                bday = bday.string
                if len(bday) < 5:
                    if len(bday[:bday.find('/')]) < 2:
                        bday = '0' + bday
                    if len(bday[bday.find('/')+1:]) < 2:
                        bday = bday[:bday.find('/')+1] + '0' + bday[-1]
            except ValueError:
                return HttpResponseBadRequest('Invalid input.')
        else:
            return HttpResponseBadRequest('Invalid input.')

        member = Member.objects.get(sunet_id=request.META['WEBAUTH_USER'])
        member.phone = phone
        member.email = email
        member.bday = bday
        member.save()
        return HttpResponseRedirect('/group/contact/')
    else:
        return HttpResponseBadRequest('Invalid form.')

# @login_required
def user_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            em_from = form.cleaned_data['email_from']
            em_subject = form.cleaned_data['email_subject']
            em_content = form.cleaned_data['email_content']

            http_header = '(CONTENT_TYPE, %s)\n(CONTENT_LENGTH, %s)\n' % (request.META.get('CONTENT_TYPE'), request.META.get('CONTENT_LENGTH'))
            for key, value in request.META.items():
                if key.startswith('HTTP_'):
                    http_header += '(%s, %s)\n' % (key, request.META.get(key))    
            http_header += request.body

            em_content = 'Contact Admin from %s Website Internal\n\nFrom: %s: %s\nSubject: %s\n%s\n\nREQUEST:\n%s' % (env('SERVER_NAME'), request.user, em_from, em_subject, em_content, http_header)
            send_mail('{%s} SYSTEM: Internal Email Notice' % env('SERVER_NAME'), em_content, EMAIL_HOST_USER, [EMAIL_NOTIFY])
            messages = 'success'
        else:
            messages = 'invalid'

        return HttpResponse(simplejson.dumps({'messages':messages}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    else:
        return HttpResponseBadRequest('Invalid form.')

# @login_required
def user_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            em_title = form.cleaned_data['upload_title']
            em_presenter = form.cleaned_data['upload_presenter']
            em_date = form.cleaned_data['upload_date']
            em_file = form.cleaned_data['upload_file']
            em_link = form.cleaned_data['upload_link']
            try:
                tmp = Presentation(title=em_title, presenter=em_presenter, date=em_date, ppt=em_file, link=em_link)
                tmp.save()
                send_mail('{%s} SYSTEM: Archive Upload Notice' % env('SERVER_NAME'), 'This is an automatic email notification for a user uploaded Presentation Archive item.\n\nThe description is:\nTitle:\t%s\nDate:\t%s\nPresenter:\t%s\nFile:\t%s\nLink:\t%s\n\nUploaded by:%s\n\n%s Website Admin\n' % (em_title, em_date, em_presenter, em_file, em_link, request.user.username, env('SERVER_NAME')), EMAIL_HOST_USER, [EMAIL_NOTIFY])
                messages = 'success'
            except:
                print traceback.format_exc()
                messages = 'invalid'
        else:
            messages = 'error'

        return render_to_response(PATH.HTML_PATH['upload'], {'upload_form':form, 'messages':messages}, context_instance=RequestContext(request))
    else:
        return render_to_response(PATH.HTML_PATH['upload'], {'upload_form':UploadForm(), 'messages':''}, context_instance=RequestContext(request))

# @login_required
# def user_profile(request):
#     profile = Member.objects.filter(sunet_id=request.user.username)
#     if len(profile) == 1:
#         profile = profile[0]
#         profile.image_link = os.path.basename(profile.image.name)
#         if not profile.description: profile.description = '(N/A)'
#         if not profile.department: profile.department = '(N/A)'
#         if not profile.more_info: profile.more_info = '(N/A)'
#         if not profile.joint_lab: profile.joint_lab = '(N/A)'
#         if not profile.start_year: profile.start_year = '(N/A)'
#         if not profile.finish_year: profile.finish_year = '(N/A)'
#         if profile.alumni:
#             profile.alumni = '<span class="label label-danger">Almuni</span>'
#         else:
#             profile.alumni = '<span class="label label-success">Current</span>'
#     else:
#         profile = []
#     return render_to_response(PATH.HTML_PATH['profile'], {'profile':profile}, context_instance=RequestContext(request))

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


@user_passes_test(lambda u: u.is_superuser)
def browse(request, path):
    fm = FileManager(MEDIA_ROOT + '/data')
    return fm.render(request, path)


def ping_test(request):
    return HttpResponse(content="", status=200)


# @login_required
def aws_dash(request):
    json = dash_aws(request)
    if isinstance(json, HttpResponseBadRequest): return json
    return HttpResponse(json, content_type='application/json')

# @login_required
def ga_dash(request):
    json = dash_ga(request)
    if isinstance(json, HttpResponseBadRequest): return json
    return HttpResponse(json, content_type='application/json')

# @login_required
def git_dash(request):
    json = dash_git(request)
    if isinstance(json, HttpResponseBadRequest):
        return json
    elif isinstance(json, HttpResponseServerError):
        i = 0
        while (isinstance(json, HttpResponseServerError) and i <= 5):
            i += 1
            sleep(1)
            json = dash_git(request)
        if isinstance(json, HttpResponseServerError): return json
    return HttpResponse(json, content_type='application/json')

# @login_required
def slack_dash(request):
    return HttpResponse(dash_slack(request), content_type='application/json')

# @login_required
def dropbox_dash(request):
    return HttpResponse(dash_dropbox(request), content_type='application/json')

# @login_required
def gcal_dash(request):
    return HttpResponse(dash_cal(), content_type='application/json')

# @login_required
def user_dash(request):
    # if request.user.username == u'daslab': return HttpResponseBadRequest('Fake admin login.')
    try:
        sunet_id = request.META['WEBAUTH_USER']
        if sunet_id in GROUP.ADMIN:
            user_type = 'admin'
        elif sunet_id in GROUP.GROUP:
            user_type = 'group'
        elif sunet_id in GROUP.ALUMNI:
            user_type = 'alumni'
        elif sunet_id in GROUP.ROTON:
            user_type = 'roton'
        elif sunet_id in GROUP.OTHER:
            user_type = 'other'
        else:
            user_type = 'unknown'

        user = Member.objects.get(sunet_id=sunet_id)
        if user.phone:
            user.phone = str(user.phone)
            user.phone = '(%s) %s-%s' % (user.phone[:3], user.phone[3:6], user.phone[6:])
        user.type = user_type

        json = {'id':user.sunet_id, 'type':user.type, 'title':user.affiliation(), 'name':user.full_name(), 'photo':user.image_tag(), 'email':user.email, 'phone':user.phone, 'bday':user.bday, 'cap':user.more_info, 'status':user.year()}
    except:
        if request.META.has_key('WEBAUTH_USER'):
            json = {'id':sunet_id, 'type':user_type}
        else:
            json = {}
    return HttpResponse(simplejson.dumps(json, sort_keys=True, indent=' ' * 4), content_type='application/json')

# @login_required
def schedule_dash(request):
    json = dash_schedule(request)
    flash_slide = FlashSlide.objects.order_by('-date')[0]
    flash_slide = {'url':flash_slide.link, 'date':flash_slide.date.strftime('%Y-%m-%d')}
    journal_club = JournalClub.objects.order_by('-date')[0]
    journal_club = {'url':journal_club.link, 'date':journal_club.date.strftime('%Y-%m-%d'), 'name':journal_club.presenter, 'title':journal_club.title}
    eterna = EternaYoutube.objects.order_by('-date')[0]
    eterna = {'url':eterna.link, 'date':eterna.date.strftime('%Y-%m-%d'), 'name':eterna.presenter, 'title':eterna.title}
    rotation = RotationStudent.objects.order_by('-date')[0]
    rotation = {'date':rotation.date.strftime('%Y-%m-%d'), 'name':rotation.full_name, 'title':rotation.title, 'url':os.path.basename(rotation.ppt.name)}
    archive = Presentation.objects.order_by('-date')[0]
    if archive.ppt:
        ar_link = os.path.basename(archive.ppt.name)
    else:
        ar_link = archive.link
    archive = {'date':archive.date.strftime('%Y-%m-%d'), 'name':archive.presenter, 'title':archive.title, 'url':ar_link}
    json.update({'flash_slide':flash_slide, 'journal_club':journal_club, 'eterna':eterna, 'rotation':rotation, 'archive':archive}) 
    return HttpResponse(simplejson.dumps(json, sort_keys=True, indent=' ' * 4), content_type='application/json')


def get_admin(request):
    return HttpResponse(simplejson.dumps({'email':EMAIL_NOTIFY}, sort_keys=True, indent=' ' * 4), content_type='application/json')

def get_user(request):
    if request.META.has_key('WEBAUTH_USER'):
        user = request.META['WEBAUTH_USER']
    else:
        user = 'unknown'
    return HttpResponse(simplejson.dumps({'user':user}, sort_keys=True, indent=' ' * 4), content_type='application/json')

def get_js(request):
    lines = open('%s/cache/stat_sys.txt' % MEDIA_ROOT, 'r').readlines()
    lines = ''.join(lines).split('\t')
    json = {'jquery':lines[11], 'bootstrap':lines[12], 'swfobj':lines[16], 'fullcal':lines[17], 'moment':lines[18]}
    return HttpResponse(simplejson.dumps(json, sort_keys=True, indent=' ' * 4), content_type='application/json')


def error400(request):
    return render_to_response(PATH.HTML_PATH['400'], {}, context_instance=RequestContext(request))
def error401(request):
    return render_to_response(PATH.HTML_PATH['401'], {}, context_instance=RequestContext(request))
def error403(request):
    return render_to_response(PATH.HTML_PATH['403'], {}, context_instance=RequestContext(request))
def error404(request):
    return render_to_response(PATH.HTML_PATH['404'], {}, context_instance=RequestContext(request))
def error500(request):
    return render_to_response(PATH.HTML_PATH['500'], {}, context_instance=RequestContext(request))
def error503(request):
    return render_to_response(PATH.HTML_PATH['503'], {}, context_instance=RequestContext(request))


def test(request):
    print request.META
    # get_sys_crontab()
    raise ValueError
    return error400(request)
    # send_notify_emails('test', 'test')
    # send_mail('text', 'test', EMAIL_HOST_USER, [EMAIL_NOTIFY])
    return HttpResponse(content="", status=200)

