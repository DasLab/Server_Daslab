from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render

import re
import traceback

from filemanager import FileManager

from src.models import *
from src.env import error400, error403


def user_sunetid(request):
    # return 't47'
    if 'WEBAUTH_USER' in request.META:
        return request.META['WEBAUTH_USER']
    elif 'REMOTE_USER' in request.META:
        return request.META['REMOTE_USER']
    elif 'sunet_id' in request.session:
        return request.session['sunet_id']
    else:
        return None


def user_login(request):
    if not hasattr(request, 'user'):
        return error403(request)

    if request.user.is_authenticated():
        if 'next' in request.GET and 'admin' in request.GET.get('next'):
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
                    if flag == 'Admin':
                        return HttpResponseRedirect('/admin/')
                    else:
                        return HttpResponseRedirect('/group/')
                else:
                    messages = 'Inactive/disabled account. Please contact us.'
        return render(request, PATH.HTML_PATH['login'], {'form': form, 'messages': messages})
    else:
        if 'next' in request.GET and 'admin' in request.GET.get('next'):
            flag = 'Admin'
        else:
            flag = 'Member'
        form = LoginForm(initial={'flag': flag})
        return render(request, PATH.HTML_PATH['login'], {'form': form})

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
                return render(request, PATH.HTML_PATH['password'], {'form': form, 'messages': 'New password does not match. Please try again.'})
            if password_new == password_old:
                return render(request, PATH.HTML_PATH['password'], {'form': form, 'messages': 'New password is the same as current. Please try again.'})

            user = authenticate(username=username, password=password_old)
            if user is not None:
                u = User.objects.get(username=username)
                u.set_password(password_new)
                u.save()
                logout(request)
                return render(request, PATH.HTML_PATH['password'], {'form': form, 'notices': 'Password change successful. Please sign in using new credentials.'})
        form = PasswordForm(initial={'username': request.user.username})
        return render(request, PATH.HTML_PATH['password'], {'form': form, 'messages': 'Invalid username and/or current password, or missing new password.<br/>Please try again.'})
    else:
        form = PasswordForm(initial={'username': request.user.username})
        return render(request, PATH.HTML_PATH['password'], {'form': form})

# @login_required
def user_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['contact_email']
                phone = form.cleaned_data['contact_phone']
                bday = form.cleaned_data['contact_bday']
                bday = re.match('[0-9]{1,2}\/[0-9]{1,2}', bday)
                if bday is None:
                    raise ValueError
                bday = bday.string
                if len(bday) < 5:
                    if len(bday[:bday.find('/')]) < 2:
                        bday = '0' + bday
                    if len(bday[bday.find('/')+1:]) < 2:
                        bday = bday[:bday.find('/')+1] + '0' + bday[-1]
            except ValueError:
                return error400(request)
        else:
            return error400(request)

        member = Member.objects.get(sunet_id=user_sunetid(request))
        member.phone = phone
        member.email = email
        member.bday = bday
        member.save()
        return HttpResponseRedirect('/group/contact/')
    else:
        return error400(request)

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
            send_mail(
                '{%s} SYSTEM: Internal Email Notice' % env('SERVER_NAME'),
                em_content,
                EMAIL_HOST_USER, [EMAIL_NOTIFY]
            )
            messages = 'success'
        else:
            messages = 'invalid'

        return HttpResponse(simplejson.dumps({'messages': messages}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    else:
        return error400(request)

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
                send_mail(
                    '{%s} SYSTEM: Archive Upload Notice' % env('SERVER_NAME'),
                    'This is an automatic email notification for a user uploaded Presentation Archive item.\n\nThe description is:\nTitle:\t%s\nDate:\t%s\nPresenter:\t%s\nFile:\t%s\nLink:\t%s\n\nUploaded by:%s\n\n%s Website Admin\n' % (em_title, em_date, em_presenter, em_file, em_link, request.user.username, env('SERVER_NAME')),
                    EMAIL_HOST_USER, [EMAIL_NOTIFY]
                )
                messages = 'success'
            except Exception:
                print traceback.format_exc()
                messages = 'invalid'
        else:
            messages = 'error'

        return HttpResponse(simplejson.dumps({'messages': messages}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    else:
        return render(request, PATH.HTML_PATH['upload'], {'upload_form': UploadForm(), 'messages': ''})

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
#     return render(request, PATH.HTML_PATH['profile'], {'profile':profile})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@user_passes_test(lambda u: u.is_superuser)
def browse(request, path):
    fm = FileManager(MEDIA_ROOT + '/data')
    return fm.render(request, path)


