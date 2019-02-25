from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from src.auth import get_user_sunetid
from src.console import *
from src.dash import *
from src.env import error400, error401, error403, error404, error500, error503
from src.models import *
from src.settings import *
from src.user import user_contact


def index(request):
    return render(request, PATH.HTML_PATH['index'])

def pages(request, keyword):
    keyword = keyword.strip('/')
    json = {}
    if keyword == 'news':
        news_list = News.objects.filter(is_visible=1).order_by('-date')
        for news in news_list:
            if news.image:
                news.image_link = os.path.basename(news.image.name)
        json = {'news_list': news_list}

    elif keyword == 'people':
        member = Member.objects.filter(is_alumni=0, is_visible=1).order_by('last_name', 'first_name')
        almuni = Member.objects.filter(is_alumni=1, is_visible=1).order_by('finish_year', '-start_year')
        for ppl in member:
            if ppl.image:
                ppl.image_link = os.path.basename(ppl.image.name)
        json = {
            'current_member': member,
            'past_member': almuni,
        }

    elif keyword == 'publications':
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
        json = {'pub_list': pub_list}

    return render(request, PATH.HTML_PATH[keyword], json)


def group_index(request):
    return render(request, PATH.HTML_PATH['group_index'])

@login_required
def group_pages(request, path):
    path = path.strip('/')
    for key in PATH.GROUP_PATH:
        if path in PATH.GROUP_PATH[key]:
            break
    page = '%s_%s' % (key, path) if key != path else path
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
                gp.label = PATH.COLOR[gp.date.month - 1]
            if i == len(flash_list) - 1 or flash_list[i + 1].date.month != gp.date.month:
                gp.month_end = True
        json = {'flash_list': flash_list}

    elif path == 'journal_club':
        jc_list = JournalClub.objects.order_by('-date')
        for i, gp in enumerate(jc_list):
            gp.label = PATH.COLOR[11 - i % 12]
            if i == 0 or jc_list[i - 1].date.year != gp.date.year:
                gp.year_start = True
        json = {'jc_list': jc_list}

    elif path == 'eterna_youtube':
        eterna_list = EternaYoutube.objects.order_by('-date')
        for i, gp in enumerate(eterna_list):
            gp.label = PATH.COLOR[11 - i % 12]
            if i == 0 or eterna_list[i - 1].date.year != gp.date.year:
                gp.year_start = True
        json = {'eterna_list': eterna_list}

    elif path == 'rotation':
        rot_list = RotationStudent.objects.order_by('-date')
        for i, rot in enumerate(rot_list):
            rot.label = PATH.COLOR[11 - i % 12]
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
            arv.label = PATH.COLOR[11 - i % 12]
            if i == 0 or arv_list[i - 1].date.year != arv.date.year:
                arv.year_start = True
            if arv.ppt:
                arv.ppt_link = os.path.basename(arv.ppt.name).replace('C:\\fakepath\\', '')
        json = {'arv_list': arv_list}

    elif path == 'defense':
        pos_list = DefensePoster.objects.order_by('-date')
        for i, pos in enumerate(pos_list):
            pos.label = PATH.COLOR[11 - i % 12]
            if i == 0 or pos_list[i - 1].date.year != pos.date.year:
                pos.year_start = True
            if pos.image:
                pos.image_link = os.path.basename(pos.image.name).replace('C:\\fakepath\\', '')
        json = {'pos_list': pos_list}

    elif path == 'contact':
        if request.method == 'POST':
            return user_contact(request)

        member = Member.objects.filter(is_alumni=0).order_by('last_name', 'first_name')
        for i, ppl in enumerate(member):
            ppl.label = PATH.COLOR[11 - i % 12]
            ppl.name = ppl.full_name()
            ppl.photo = ppl.image_tag()
            ppl.title = ppl.affiliation()
            ppl.status = ppl.year()
            ppl.type = GROUP.find_type(ppl.sunet_id)
            if ppl.phone:
                ppl.phone = str(ppl.phone)
                ppl.phone = '(%s) %s-%s' % (ppl.phone[:3], ppl.phone[3:6], ppl.phone[6:])
        almuni = Member.objects.filter(is_alumni=1).order_by('-finish_year', 'start_year')
        for i, ppl in enumerate(almuni):
            ppl.label = PATH.COLOR[11 - i % 12]
            if i == 0 or almuni[i - 1].finish_year != ppl.finish_year:
                ppl.year_start = True
            ppl.name = ppl.full_name()
            ppl.photo = ppl.image_tag()
            ppl.title = ppl.affiliation()
            ppl.status = ppl.year()
            if ppl.phone:
                ppl.phone = str(ppl.phone)
                ppl.phone = '(%s) %s-%s' % (ppl.phone[:3], ppl.phone[3:6], ppl.phone[6:])
        json = {
            'current_member': member,
            'past_member': almuni,
            'contact_form':  ContactForm(),
            'sunet_id': get_user_sunetid(request),
        }

    return render(request, PATH.HTML_PATH['group_pages'].replace('xxx', page), json)

@login_required
def group_dash(request, keyword):
    keyword = keyword.strip('/')
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
        flash_slide = {
            'url': flash_slide.link,
            'date': flash_slide.date.strftime('%Y-%m-%d'),
        }
        journal_club = JournalClub.objects.order_by('-date')[0]
        journal_club = {
            'url': journal_club.link,
            'date': journal_club.date.strftime('%Y-%m-%d'),
            'name': journal_club.presenter,
            'title': journal_club.title,
        }
        eterna = EternaYoutube.objects.order_by('-date')[0]
        eterna = {
            'url': eterna.link,
            'date': eterna.date.strftime('%Y-%m-%d'),
            'name': eterna.presenter,
            'title': eterna.title,
        }
        rotation = RotationStudent.objects.order_by('-date')[0]
        rotation = {
            'date': rotation.date.strftime('%Y-%m-%d'),
            'name': rotation.full_name,
            'title': rotation.title,
            'url': os.path.basename(rotation.ppt.name),
        }
        archive = Presentation.objects.order_by('-date')[0]
        if archive.ppt:
            ar_link = os.path.basename(archive.ppt.name)
        else:
            ar_link = archive.link
        archive = {
            'date': archive.date.strftime('%Y-%m-%d'),
            'name': archive.presenter,
            'title': archive.title,
            'url': ar_link,
        }
        json.update({
            'flash_slide': flash_slide,
            'journal_club': journal_club,
            'eterna': eterna,
            'rotation': rotation,
            'archive': archive,
        })
        json = simplejson.dumps(json, sort_keys=True, indent=' ' * 4)

    elif keyword == 'user':
        try:
            sunet_id = get_user_sunetid(request)
            user_type = GROUP.find_type(sunet_id)
            user = Member.objects.get(sunet_id=sunet_id)
            if user.phone:
                user.phone = str(user.phone)
                user.phone = '(%s) %s-%s' % (user.phone[:3], user.phone[3:6], user.phone[6:])
            user.type = user_type

            json = {
                'id': user.sunet_id,
                'type': user.type,
                'title': user.affiliation(),
                'name': user.full_name(),
                'photo': user.image_tag(),
                'email': user.email,
                'phone': user.phone,
                'bday': user.bday,
                'cap': user.more_info,
                'status': user.year(),
            }
        except Exception:
            json = {'type': 'unknown'} if sunet_id is None else {'id': sunet_id, 'type': user_type}
        json = simplejson.dumps(json, sort_keys=True, indent=' ' * 4)

    elif keyword == 'secret':
        (gmail, db) = (env.email_url(), env.db())
        json = {
            'mysql': {
                'user': db['USER'],
                'password': db['PASSWORD'],
            },
            'apache': {
                'user': env('APACHE_USER'),
                'password': env('APACHE_PASSWORD'),
            },
            'django': {
                'member': {
                    'user': env('DJANGO_MEMBER_USER'),
                    'password': env('DJANGO_MEMBER_PASSWORD'),
                },
                'admin': {
                    'user': env('DJANGO_ADMIN_USER'),
                    'password': env('DJANGO_ADMIN_PASSWORD'),
                },
            },
            'gmail': {
                'user': gmail['EMAIL_HOST_USER'],
                'password': gmail['EMAIL_HOST_PASSWORD'],
            },
            'vendor': {
                'user': gmail['EMAIL_HOST_USER'],
                'password': GIT['PASSWORD'],
            },
        }
        json = simplejson.dumps(json, sort_keys=True, indent=' ' * 4)

    if isinstance(json, HttpResponse):
        return json
    return HttpResponse(json, content_type='application/json')


def ping_test(request):
    return HttpResponse(content='', status=200)


def get_staff(request):
    user = get_user_sunetid(request)
    user = 'unknown' if user is None else user
    json = {
        'user': user,
        'admin': EMAIL_NOTIFY,
    }
    return HttpResponse(simplejson.dumps(json, sort_keys=True, indent=' ' * 4), content_type='application/json')



def test(request):
    print request.META
    # get_sys_crontab()
    raise ValueError
    return error400(request)
    # send_notify_emails('test', 'test')
    # send_mail('text', 'test', EMAIL_HOST_USER, [EMAIL_NOTIFY])
    return HttpResponse(content='', status=200)

