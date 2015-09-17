from django.conf.urls import include, url, handler404, handler500
# from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login
# from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from adminplus.sites import AdminSitePlus
from filemanager import path_end

from settings import MEDIA_ROOT, STATIC_ROOT, STATIC_URL, DEBUG
from src import views

admin.site = AdminSitePlus()
admin.site.index_title = 'Das Lab Website Administration'
admin.autodiscover()
admin.site.login = views.user_login
admin.site.logout = views.user_logout


urlpatterns = [
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^home/$', views.index),
    url(r'^research/$', views.research),
    url(r'^news/$', views.news),
    url(r'^people/$', views.people),
    url(r'^publications/$', views.publications),
    url(r'^resources/$', views.resources),
    url(r'^contact/$', views.contact),

    url(r'^index\.html$', RedirectView.as_view(url='/index/', permanent=True)),
    url(r'^das_research\.html$', RedirectView.as_view(url='/research/', permanent=True)),
    url(r'^das_news\.html$', RedirectView.as_view(url='/news/', permanent=True)),
    url(r'^das_people\.html$', RedirectView.as_view(url='/people/', permanent=True)),
    url(r'^das_publications\.html$', RedirectView.as_view(url='/publications/', permanent=True)),
    url(r'^das_resources\.html$', RedirectView.as_view(url='/resources/', permanent=True)),
    url(r'^das_contact\.html$', RedirectView.as_view(url='/contact/', permanent=True)),
    url(r'^member/$', RedirectView.as_view(url='/people/', permanent=True)),

    url(r'^login/$', views.user_login),
    url(r'^password/$', views.user_password),
    url(r'^update_contact/$', views.user_contact),
    url(r'^email_admin/$', views.user_email),
    url(r'^get_admin/$', views.get_admin),
    url(r'^profile/$', views.user_profile),
    url(r'^logout/$', views.user_logout),
    
    url(r'^group/$', views.lab_home),
    url(r'^group/schedule/$', views.lab_meeting_schedule),
    url(r'^group/flash_slide/$', views.lab_meeting_flash),
    url(r'^group/youtube/$', views.lab_meeting_youtube),
    url(r'^group/rotation/$', views.lab_meeting_rotation),
    url(r'^group/calendar/$', views.lab_calendar),
    url(r'^group/gdocs/$', views.lab_resource_gdocs),
    url(r'^group/archive/$', views.lab_resource_archive),
    url(r'^group/contact/$', views.lab_resource_contact),
    url(r'^group/aws/$', views.lab_server_aws),
    url(r'^group/ga/$', views.lab_server_ga),
    url(r'^group/git/$', views.lab_service_git),
    url(r'^group/slack/$', views.lab_service_slack),
    url(r'^group/dropbox/$', views.lab_service_dropbox),
    url(r'^group/misc/$', views.lab_misc),

    url(r'^ping_test/$', views.ping_test),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT + '/media'}),
    url(r'^site_data/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT + '/data'}),

    url(r'^admin/browse/' + path_end, views.browse),
    url(r'^admin/aws_dash/$', views.aws_dash),
    url(r'^admin/ga_dash/$', views.ga_dash),
    url(r'^admin/git_dash/$', views.git_dash),
    url(r'^admin/slack_dash/$', views.slack_dash),
    url(r'^admin/dropbox_dash/$', views.dropbox_dash),
    url(r'^admin/user_dash/$', views.user_dash),
    url(r'^admin/schedule_dash/$', views.schedule_dash),
    url(r'^admin/gcal/$', views.gcal),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?:robots.txt)?$', 'django.views.static.serve', kwargs={'path': 'robots.txt', 'document_root': MEDIA_ROOT}),

] #+ static(STATIC_URL, document_root=STATIC_ROOT)

if DEBUG: urlpatterns.append(url(r'^test/$', views.test))
handler404 = views.error404
handler500 = views.error500

