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

    url(r'^login/$', views.user_login),
    url(r'^password/$', views.user_password),
    url(r'^profile/$', views.user_profile),
    url(r'^logout/$', views.user_logout),
    
    url(r'^group/meetings/$', views.lab_meetings),
    url(r'^group/calendar/$', views.lab_calendar),
    url(r'^group/documents/$', views.lab_documents),
    url(r'^group/services/$', views.lab_services),
    url(r'^group/servers/$', views.lab_servers),
    url(r'^group/misc/$', views.lab_misc),
    url(r'^group/$', RedirectView.as_view(url='/group/meetings/', permanent=True)),

    url(r'^ping_test/$', views.ping_test),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT + '/media'}),
    url(r'^site_data/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT + '/data'}),

    url(r'^admin/browse/' + path_end, views.browse),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?:robots.txt)?$', 'django.views.static.serve', kwargs={'path': 'robots.txt', 'document_root': MEDIA_ROOT}),

] #+ static(STATIC_URL, document_root=STATIC_ROOT)

if DEBUG: urlpatterns.append(url(r'^test/$', views.test))
handler404 = views.error404
handler500 = views.error500

