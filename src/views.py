from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render

from src.console import *
from src.dash import *
from src.env import error400, error401, error403, error404, error500, error503
from src.models import *
from src.settings import *

colors = ('brown', 'dark-red', 'danger', 'orange', 'warning', 'green', 'success', 'light-blue', 'info', 'primary', 'dark-blue', 'violet')


def index(request):
    return render(request, PATH.HTML_PATH['index'])
def research(request):
    return render(request, PATH.HTML_PATH['research'])
def resources(request):
    return render(request, PATH.HTML_PATH['resources'])
def contact(request):
    return render(request, PATH.HTML_PATH['contact'])

def news(request):
    news_list = News.objects.filter(is_visible=1).order_by('-date')
    for news in news_list:
        if news.image:
            news.image_link = os.path.basename(news.image.name)
    return render(request, PATH.HTML_PATH['news'], {'news_list': news_list})

def people(request):
    member = Member.objects.filter(is_alumni=0, is_visible=1).order_by('last_name', 'first_name')
    almuni = Member.objects.filter(is_alumni=1, is_visible=1).order_by('finish_year', 'start_year')
    for ppl in member:
        if ppl.image:
            ppl.image_link = os.path.basename(ppl.image.name)
    return render(request, PATH.HTML_PATH['people'], {'current_member': member, 'past_member': almuni})

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
    return render(request, PATH.HTML_PATH['publications'], {'pub_list': pub_list})


############################################################################################################################################

# @login_required
def group_index(request):
    return render(request, PATH.HTML_PATH['group_index'])

# @login_required
def group_pages(request, path):
    for key in PATH.GROUP_PATH:
        if path in PATH.GROUP_PATH[key]:
            break
    page = path
    if key != path: page = '%s_%s' % (key, path)
    json = {}

    if path == 'flash_slide':
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
        json = {'flash_list': flash_list}
    elif path == 'journal_club':
        jc_list = JournalClub.objects.order_by('-date')
        for i, gp in enumerate(jc_list):
            gp.label = colors[11 - i % 12]
            if i == 0 or jc_list[i - 1].date.year != gp.date.year:
                gp.year_start = True
        json = {'jc_list': jc_list}
    elif path == 'eterna_youtube':
        eterna_list = EternaYoutube.objects.order_by('-date')
        for i, gp in enumerate(eterna_list):
            gp.label = colors[11 - i % 12]
            if i == 0 or eterna_list[i - 1].date.year != gp.date.year:
                gp.year_start = True
        json = {'eterna_list': eterna_list}
    elif path == 'rotation':
        rot_list = RotationStudent.objects.order_by('-date')
        for i, rot in enumerate(rot_list):
            rot.label = colors[11 - i % 12]
            if i == 0 or rot_list[i - 1].date.year != rot.date.year:
                rot.year_start = True
            if rot.ppt:
                rot.ppt_link = os.path.basename(rot.ppt.name)
            if rot.data:
                rot.dat_link = os.path.basename(rot.data.name)
        json = {'rot_list': rot_list}
    elif path == 'archive':
        arv_list = Presentation.objects.order_by('-date')
        for i, arv in enumerate(arv_list):
            arv.label = colors[11 - i % 12]
            if i == 0 or arv_list[i - 1].date.year != arv.date.year:
                arv.year_start = True
            if arv.ppt:
                arv.ppt_link = os.path.basename(arv.ppt.name).replace('C:\\fakepath\\', '')
        json = {'arv_list': arv_list}
    elif path == 'contact':
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
        json = {'current_member': member, 'past_member': almuni, 'contact_form':  ContactForm()}

    return render(request, PATH.HTML_PATH['group_pages'].replace('xxx', page), json)

def group_dash(request, keyword):
    if keyword == 'aws':
        json = dash_aws(request)
    elif keyword == 'ga':
        json = dash_ga(request)
    elif keyword == 'git':
        json = dash_git(request)
    elif keyword == 'slack':
        json = dash_slack(request)
    elif keyword == 'dropbox':
        json = dash_dropbox(request)
    elif keyword == 'gcal':
        json = dash_cal()
    elif keyword == 'schedule':
        json = dash_schedule(request)
        flash_slide = FlashSlide.objects.order_by('-date')[0]
        flash_slide = {'url': flash_slide.link, 'date': flash_slide.date.strftime('%Y-%m-%d')}
        journal_club = JournalClub.objects.order_by('-date')[0]
        journal_club = {'url': journal_club.link, 'date': journal_club.date.strftime('%Y-%m-%d'), 'name': journal_club.presenter, 'title': journal_club.title}
        eterna = EternaYoutube.objects.order_by('-date')[0]
        eterna = {'url': eterna.link, 'date': eterna.date.strftime('%Y-%m-%d'), 'name': eterna.presenter, 'title': eterna.title}
        rotation = RotationStudent.objects.order_by('-date')[0]
        rotation = {'date': rotation.date.strftime('%Y-%m-%d'), 'name': rotation.full_name, 'title': rotation.title, 'url': os.path.basename(rotation.ppt.name)}
        archive = Presentation.objects.order_by('-date')[0]
        if archive.ppt:
            ar_link = os.path.basename(archive.ppt.name)
        else:
            ar_link = archive.link
        archive = {'date': archive.date.strftime('%Y-%m-%d'), 'name': archive.presenter, 'title': archive.title, 'url': ar_link}
        json.update({'flash_slide': flash_slide, 'journal_club': journal_club, 'eterna': eterna, 'rotation': rotation, 'archive': archive})
        json = simplejson.dumps(json, sort_keys=True, indent=' ' * 4)
    elif keyword == 'user':
        try:
            sunet_id = request.META['WEBAUTH_USER']
            user_type = GROUP.find_type(sunet_id)
            user = Member.objects.get(sunet_id=sunet_id)
            if user.phone:
                user.phone = str(user.phone)
                user.phone = '(%s) %s-%s' % (user.phone[:3], user.phone[3:6], user.phone[6:])
            user.type = user_type

            json = {'id': user.sunet_id, 'type': user.type, 'title': user.affiliation(), 'name': user.full_name(), 'photo': user.image_tag(), 'email': user.email, 'phone': user.phone, 'bday': user.bday, 'cap': user.more_info, 'status': user.year()}
        except Exception:
            if 'WEBAUTH_USER' in request.META:
                json = {'id': sunet_id, 'type': user_type}
            else:
                json = {'type': 'unknown'}
        json = simplejson.dumps(json, sort_keys=True, indent=' ' * 4)

    if isinstance(json, HttpResponse): return json
    return HttpResponse(json, content_type='application/json')


def ping_test(request):
    return HttpResponse(content="", status=200)


def get_staff(request):
    if 'WEBAUTH_USER' in request.META:
        user = request.META['WEBAUTH_USER']
    else:
        user = 'unknown'
    return HttpResponse(simplejson.dumps({'user': user, 'admin': EMAIL_NOTIFY}, sort_keys=True, indent=' ' * 4), content_type='application/json')



def test(request):
    print request.META
    # get_sys_crontab()
    raise ValueError
    return error400(request)
    # send_notify_emails('test', 'test')
    # send_mail('text', 'test', EMAIL_HOST_USER, [EMAIL_NOTIFY])
    return HttpResponse(content="", status=200)

