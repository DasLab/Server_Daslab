from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect
from django.template import RequestContext#, Template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
# from django.core.urlresolvers import reverse
# from django.core.mail import send_mail
from django.shortcuts import render, render_to_response, redirect
# from django import forms

from src.models import *
from src.settings import *

import datetime
import simplejson
import sys
import time
import traceback
# from sys import stderr


def index(request):
	return render_to_response(PATH.HTML_PATH['index'], {}, context_instance=RequestContext(request))
def research(request):
	return render_to_response(PATH.HTML_PATH['research'], {}, context_instance=RequestContext(request))
def resources(request):
	return render_to_response(PATH.HTML_PATH['resources'], {}, context_instance=RequestContext(request))
def contact(request):
	return render_to_response(PATH.HTML_PATH['contact'], {}, context_instance=RequestContext(request))

def people(request):
	member = CurrentMember.objects.order_by('last_name', 'first_name')
	for ppl in member:
		ppl.image_link = ppl.image.url.replace(PATH.DATA_DIR['MEMBER_IMG_DIR'], '')
	alumni = PastMember.objects.order_by('finish_year', 'start_year', 'full_name')
	return render_to_response(PATH.HTML_PATH['people'], {'current_member':member, 'past_member':alumni}, context_instance=RequestContext(request))


# def url_redirect(request, path):
# 	if 'detail/' in path:
# 		path = path.rstrip('/')
# 	if request.GET.get('searchtext'):
# 		path = path + '?searchtext=' + request.GET.get('searchtext')
# 	return HttpResponsePermanentRedirect("/%s" % path)

# def error404(request):
# 	return render_to_response(PATH.HTML_PATH['404'], {}, context_instance=RequestContext(request))

# def error500(request):
# 	# exc_type, exc_value, exc_tb = sys.exc_info()
# 	# body = '%s\n%s\n%s\n' % (exc_value, exc_type, traceback.format_exception(exc_type, exc_value, exc_tb))
# 	# send_mail('Subject', body, EMAIL_HOST_USER, [EMAIL_NOTIFY])
# 	return render_to_response(PATH.HTML_PATH['500'], {}, context_instance=RequestContext(request))



