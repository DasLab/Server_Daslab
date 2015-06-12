from django.conf.urls import patterns, include, url, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
# from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
# admin.autodiscover()

from settings import MEDIA_ROOT, STATIC_ROOT, STATIC_URL
from src import views

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

    # (r'^login/$', views.user_login),
    # (r'^register/$', views.register),
    # (r'^logout/$', views.user_logout),

    (r'^ping_test/$', views.ping_test),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT+'/media'}),
    # (r'^site_data/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),

    url(r'^admin/', include(admin.site.urls)),
    # (r'^static/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT+'/media/admin'}),
    url(r'^(?:robots.txt)?$', 'django.views.static.serve', kwargs={'path': 'robots.txt', 'document_root': MEDIA_ROOT}),
) + static(STATIC_URL, document_root=STATIC_ROOT)

# handler404 = views.error404
# handler500 = views.error500

