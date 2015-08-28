from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext#, Template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
# from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.shortcuts import render, render_to_response, redirect
# from django import forms

from filemanager import FileManager

from src.console import *
# from src.cron import *
from src.models import *
from src.settings import *

import datetime
import subprocess
import sys
import traceback
# from sys import stderr


def index(request):
	return render_to_response(PATH.HTML_PATH['index'], {'tracking_id':GA['TRACKING_ID']}, context_instance=RequestContext(request))
def research(request):
	return render_to_response(PATH.HTML_PATH['research'], {'tracking_id':GA['TRACKING_ID']}, context_instance=RequestContext(request))
def resources(request):
	return render_to_response(PATH.HTML_PATH['resources'], {'tracking_id':GA['TRACKING_ID']}, context_instance=RequestContext(request))
def contact(request):
	return render_to_response(PATH.HTML_PATH['contact'], {'tracking_id':GA['TRACKING_ID']}, context_instance=RequestContext(request))

def news(request):
	news_list = News.objects.order_by('-date')
	for news in news_list:
		if news.image:
			news.image_link = os.path.basename(news.image.name)
	return render_to_response(PATH.HTML_PATH['news'], {'tracking_id':GA['TRACKING_ID'], 'news_list':news_list}, context_instance=RequestContext(request))

def people(request):
	member = Member.objects.filter(alumni=0).order_by('last_name', 'first_name')
	almuni = Member.objects.filter(alumni=1).order_by('finish_year', 'start_year')
	for ppl in member:
		if ppl.image:
			ppl.image_link = os.path.basename(ppl.image.name)
	return render_to_response(PATH.HTML_PATH['people'], {'tracking_id':GA['TRACKING_ID'], 'current_member':member, 'past_member':almuni}, context_instance=RequestContext(request))

def publications(request):
	pub_list = Publication.objects.order_by('-display_date')
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
	return render_to_response(PATH.HTML_PATH['publications'], {'tracking_id':GA['TRACKING_ID'], 'pub_list':pub_list}, context_instance=RequestContext(request))


############################################################################################################################################

@login_required
def lab_meetings(request):
	colors = ('brown', 'dark-red', 'danger', 'orange', 'warning', 'green', 'success', 'light-blue', 'info', 'primary', 'dark-blue', 'violet')
	flash_list = FlashSlide.objects.order_by('-date')
	for i, gp in enumerate(flash_list):
		if i == 0 or flash_list[i-1].date.year != gp.date.year:
			gp.year_start = True
			gp.row_start = True
		if i == len(flash_list)-1 or flash_list[i+1].date.year != gp.date.year:
			gp.year_end = True
			gp.row_end = True
		if i == 0 or flash_list[i-1].date.month != gp.date.month:
			gp.month_start = True
			gp.label = colors[gp.date.month-1]
			if gp.date.month in (4,8,12):
				gp.row_start = True
		if i == len(flash_list)-1 or flash_list[i+1].date.month != gp.date.month:
			gp.month_end = True 
			if gp.date.month in (1,5,9):
				gp.row_end = True

	eterna_list = EternaYoutube.objects.order_by('-date')
	rot_list = RotationStudent.objects.order_by('-date')
	for rot in rot_list:
		if rot.ppt:
			rot.ppt_link = os.path.basename(rot.ppt.name)
		if rot.data:
			rot.dat_link = os.path.basename(rot.data.name)
	arv_list = Presentation.objects.order_by('-date')
	for arv in arv_list:
		if arv.ppt:
			arv.ppt_link = os.path.basename(arv.ppt.name)
	return render_to_response(PATH.HTML_PATH['lab_meetings'], {'flash_list':flash_list, 'eterna_list':eterna_list, 'rot_list':rot_list, 'arv_list':arv_list}, context_instance=RequestContext(request))

@login_required
def lab_calendar(request):
	return render_to_response(PATH.HTML_PATH['lab_calendar'], {}, context_instance=RequestContext(request))
@login_required
def lab_resources(request):
	return render_to_response(PATH.HTML_PATH['lab_resources'], {}, context_instance=RequestContext(request))
@login_required
def lab_misc(request):
	return render_to_response(PATH.HTML_PATH['lab_misc'], {}, context_instance=RequestContext(request))


def user_login(request):
	if request.user.is_authenticated():
		if 'admin' in request.GET['next']:
			return error403(request)
		return HttpResponseRedirect('/group')

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		flag = request.POST['flag']
		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				if flag == "Admin":
					return HttpResponseRedirect('/admin')
				else:
					return HttpResponseRedirect('/group')
			else:
				messages = 'Inactive/disabled account. Please contact us.'
		else:
			messages = 'Invalid username and/or password. Please try again.'
		return render_to_response(PATH.HTML_PATH['login'], {'messages':messages, 'flag':flag}, context_instance=RequestContext(request))
	else:
		if request.GET.has_key('next') and 'admin' in request.GET['next']:
			flag = 'Admin'
		else:
			flag = 'Member'
		return render_to_response(PATH.HTML_PATH['login'], {'messages':'', 'flag':flag}, context_instance=RequestContext(request))

@login_required
def user_password(request):
	if request.method == 'POST':
		password_old = request.POST['password_old']
		password_new = request.POST['password_new']
		password_new_rep = request.POST['password_new_rep']
		if password_new != password_new_rep:
			return render_to_response(PATH.HTML_PATH['password'], {'messages':'New password does not match. Please try again.'}, context_instance=RequestContext(request))
		if password_new == password_old:
			return render_to_response(PATH.HTML_PATH['password'], {'messages':'New password is the same as current. Please try again.'}, context_instance=RequestContext(request))

		user = authenticate(username=request.user, password=password_old)
		if user is not None:
			u = User.objects.get(username=request.user)
			u.set_password(password_new)
			u.save()
			logout(request)
			return render_to_response(PATH.HTML_PATH['password'], {'notices':'Password change successful. Please sign in using new credentials.'}, context_instance=RequestContext(request))
		else:
			return render_to_response(PATH.HTML_PATH['password'], {'messages':'Invalid username and/or password. Please try again.'}, context_instance=RequestContext(request))
	else:
		return render_to_response(PATH.HTML_PATH['password'], {'messages':''}, context_instance=RequestContext(request))

def user_profile(request):
	profile = Member.objects.filter(last_name=User.objects.get(username=request.user).last_name)
	if len(profile) > 1:
		profile = profile.filter(first_name=User.objects.get(username=request.user).first_name)
	if len(profile) == 1:
		profile = profile[0]
		profile.image_link = os.path.basename(profile.image.name)
		if not profile.description: profile.description = '(N/A)'
		if not profile.department: profile.department = '(N/A)'
		if not profile.more_info: profile.more_info = '(N/A)'
		if not profile.joint_lab: profile.joint_lab = '(N/A)'
		if not profile.start_year: profile.start_year = '(N/A)'
		if not profile.finish_year: profile.finish_year = '(N/A)'
		if profile.alumni:
			profile.alumni = '<span class="label label-danger">Almuni</span>'
		else:
			profile.alumni = '<span class="label label-success">Current</span>'
	else:
		profile = []
	return render_to_response(PATH.HTML_PATH['profile'], {'profile':profile}, context_instance=RequestContext(request))

def user_logout(request):
	logout(request)
	return HttpResponseRedirect("/")


@user_passes_test(lambda u: u.is_superuser)
def browse(request, path):
	fm = FileManager(MEDIA_ROOT + '/data')
	return fm.render(request, path)


def ping_test(request):
	return HttpResponse(content="", status=200)


# def url_redirect(request, path):
# 	if 'detail/' in path:
# 		path = path.rstrip('/')
# 	if request.GET.get('searchtext'):
# 		path = path + '?searchtext=' + request.GET.get('searchtext')
# 	return HttpResponsePermanentRedirect("/%s" % path)

def error400(request):
	return render_to_response(PATH.HTML_PATH['400'], {}, context_instance=RequestContext(request))

def error401(request):
	return render_to_response(PATH.HTML_PATH['401'], {}, context_instance=RequestContext(request))

def error403(request):
	return render_to_response(PATH.HTML_PATH['403'], {}, context_instance=RequestContext(request))

def error404(request):
	return render_to_response(PATH.HTML_PATH['404'], {'tracking_id':GA['TRACKING_ID']}, context_instance=RequestContext(request))

def error500(request):
	return render_to_response(PATH.HTML_PATH['500'], {}, context_instance=RequestContext(request))


def test(request):
	return error401(request)
	raise ValueError
	# send_notify_emails('test', 'test')
	# send_mail('text', 'test', EMAIL_HOST_USER, [EMAIL_NOTIFY])
	return HttpResponse(content="", status=200)

