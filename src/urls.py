from django.conf.urls import patterns, include, url, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login
# from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from adminplus.sites import AdminSitePlus
from filemanager import path_end

from settings import MEDIA_ROOT, STATIC_ROOT, STATIC_URL
from src import views

admin.site = AdminSitePlus()
admin.site.index_title = 'Das Lab Website Administration'
admin.autodiscover()
admin.site.login = views.user_login
admin.site.logout = views.user_logout


urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^index/$', views.index),
    (r'^home/$', views.index),
    (r'^research/$', views.research),
    (r'^news/$', views.news),
    (r'^people/$', views.people),
    (r'^publications/$', views.publications),
    (r'^resources/$', views.resources),
    (r'^contact/$', views.contact),

    (r'^index\.html$', RedirectView.as_view(url='/index/', permanent=True)),
    (r'^das_research\.html$', RedirectView.as_view(url='/research/', permanent=True)),
    (r'^das_news\.html$', RedirectView.as_view(url='/news/', permanent=True)),
    (r'^das_people\.html$', RedirectView.as_view(url='/people/', permanent=True)),
    (r'^das_publications\.html$', RedirectView.as_view(url='/publications/', permanent=True)),
    (r'^das_resources\.html$', RedirectView.as_view(url='/resources/', permanent=True)),
    (r'^das_contact\.html$', RedirectView.as_view(url='/contact/', permanent=True)),

    (r'^login/$', views.user_login),
    (r'^password/$', views.user_password),
    (r'^profile/$', views.user_profile),
    (r'^logout/$', views.user_logout),
    
    (r'^group/meetings/$', views.lab_meetings),
    (r'^group/calendar/$', views.lab_calendar),
    (r'^group/resources/$', views.lab_resources),
    (r'^group/misc/$', views.lab_misc),
    (r'^group/$', RedirectView.as_view(url='/group/meetings/', permanent=True)),

    (r'^ping_test/$', views.ping_test),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT + '/media'}),
    (r'^site_data/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT + '/data'}),

    (r'^admin/browse/' + path_end, views.browse),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?:robots.txt)?$', 'django.views.static.serve', kwargs={'path': 'robots.txt', 'document_root': MEDIA_ROOT}),

) #+ static(STATIC_URL, document_root=STATIC_ROOT)

handler404 = views.error404
handler500 = views.error500

