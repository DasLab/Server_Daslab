from django.conf.urls import include, url, handler404, handler500
# from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib.auth.views import login
from django.views.generic import RedirectView
from django.views.static import serve

from adminplus.sites import AdminSitePlus
from filemanager import path_end

from src.settings import MEDIA_ROOT, STATIC_ROOT, STATIC_URL, DEBUG, IS_MAINTENANCE, env
from src import views

admin.site = AdminSitePlus()
admin.site.index_title = '%s Administration' % env('SERVER_NAME')
admin.autodiscover()
admin.site.login = views.user_login
admin.site.logout = views.user_logout


if IS_MAINTENANCE:
    urlpatterns = [
        url(r'^ping_test/?$', views.ping_test),
        url(r'^get_admin/?$', views.get_admin),
        url(r'^get_js/?$', views.get_js),

        url(r'^site_media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT + '/media'}),
        url(r'^robots.txt$', serve, kwargs={'path': 'robots.txt', 'document_root': MEDIA_ROOT}),

        url(r'^$', views.error503),
        url(r'^.*/?$', RedirectView.as_view(url='/', permanent=True)),
    ]
else:
    urlpatterns = [
        url(r'^$', views.index),
        url(r'^research/?$', views.research),
        url(r'^news/?$', views.news),
        url(r'^people/?$', views.people),
        url(r'^publications/?$', views.publications),
        url(r'^resources/?$', views.resources),
        url(r'^contact/?$', views.contact),

        url(r'^index\.html$', RedirectView.as_view(url='/index/', permanent=True)),
        url(r'^das_research\.html$', RedirectView.as_view(url='/research/', permanent=True)),
        url(r'^das_news\.html$', RedirectView.as_view(url='/news/', permanent=True)),
        url(r'^das_people\.html$', RedirectView.as_view(url='/people/', permanent=True)),
        url(r'^das_publications\.html$', RedirectView.as_view(url='/publications/', permanent=True)),
        url(r'^das_resources\.html$', RedirectView.as_view(url='/resources/', permanent=True)),
        url(r'^das_contact\.html$', RedirectView.as_view(url='/contact/', permanent=True)),

        url(r'^home/?$', RedirectView.as_view(url='/', permanent=True)),
        url(r'^index/?$', RedirectView.as_view(url='/', permanent=True)),
        url(r'^member/?$', RedirectView.as_view(url='/people/', permanent=True)),
        url(r'^members/?$', RedirectView.as_view(url='/people/', permanent=True)),
        url(r'^publication/?$', RedirectView.as_view(url='/publications/', permanent=True)),
        url(r'^resource/?$', RedirectView.as_view(url='/resources/', permanent=True)),
        url(r'^contacts/?$', RedirectView.as_view(url='/contact/', permanent=True)),
        url(r'^groups/?$', RedirectView.as_view(url='/group/', permanent=True)),
        url(r'^admin$', RedirectView.as_view(url='/admin/', permanent=True)),

        url(r'^signin/?$', views.user_login),
        url(r'^logout/?$', RedirectView.as_view(url='/index/', permanent=True)),
        url(r'^signout/?$', views.user_logout),
        url(r'^password/?$', views.user_password),
        url(r'^get_admin/?$', views.get_admin),
        url(r'^get_js/?$', views.get_js),

        url(r'^group/?$', views.lab_home),
        url(r'^group/schedule/?$', views.lab_meeting_schedule),
        url(r'^group/flash_slide/?$', views.lab_meeting_flash),
        url(r'^group/journal_club/?$', views.lab_meeting_jc),
        url(r'^group/youtube/?$', views.lab_meeting_youtube),
        url(r'^group/rotation/?$', views.lab_meeting_rotation),
        url(r'^group/calendar/?$', views.lab_calendar),
        url(r'^group/gdocs/?$', views.lab_resource_gdocs),
        url(r'^group/archive/?$', views.lab_resource_archive),
        url(r'^group/archive/upload/?$', views.user_upload),
        url(r'^group/contact/?$', views.lab_resource_contact),
        url(r'^group/contact/update/?$', views.user_contact),
        url(r'^group/aws/?$', views.lab_server_aws),
        url(r'^group/ga/?$', views.lab_server_ga),
        url(r'^group/bot/?$', views.lab_service_bot),
        url(r'^group/git/?$', views.lab_service_git),
        url(r'^group/slack/?$', views.lab_service_slack),
        url(r'^group/dropbox/?$', views.lab_service_dropbox),
        url(r'^group/misc/?$', views.lab_misc),
        url(r'^group/error/?$', views.lab_error),
        url(r'^group/email_admin/?$', views.user_email),
        url(r'^group/get_user/?$', views.get_user),

        url(r'^group/aws_dash/?$', views.aws_dash),
        url(r'^group/ga_dash/?$', views.ga_dash),
        url(r'^group/git_dash/?$', views.git_dash),
        url(r'^group/slack_dash/?$', views.slack_dash),
        url(r'^group/dropbox_dash/?$', views.dropbox_dash),
        url(r'^group/user_dash/?$', views.user_dash),
        url(r'^group/schedule_dash/?$', views.schedule_dash),
        url(r'^group/gcal_dash/?$', views.gcal_dash),

        url(r'^ping_test/?$', views.ping_test),
        url(r'^site_media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT + '/media'}),
        url(r'^site_data/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT + '/data'}),

        url(r'^error/400/?$', views.error400),
        url(r'^error/401/?$', views.error401),
        url(r'^error/403/?$', views.error403),
        url(r'^error/404/?$', views.error404),
        url(r'^error/500/?$', views.error500),
        url(r'^error/503/?$', views.error503),

        url(r'^admin/browse/' + path_end, views.browse),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^robots.txt$', serve, kwargs={'path': 'robots.txt', 'document_root': MEDIA_ROOT}),
    ] #+ static(STATIC_URL, document_root=STATIC_ROOT)

    if DEBUG: urlpatterns.append(url(r'^test/$', views.test))

handler404 = views.error404
handler500 = views.error500

