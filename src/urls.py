from django.conf.urls import patterns, include, url, handler404, handler500
from django.contrib import admin
# from django.core.urlresolvers import reverse_lazy
# from django.views.generic import RedirectView
# admin.autodiscover()

from settings import MEDIA_ROOT
from src import views

urlpatterns = patterns('',
    (r'^$', views.index),

    # (r'^login/$', views.user_login),
    # (r'^register/$', views.register),
    # (r'^logout/$', views.user_logout),

    # (r'^ping_test/$', views.test),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT+'/media'}),

    # url(r'^admin/', include(admin.site.urls)),
    # (r'^static/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT+'/media/admin'}),
    url(r'^(?:robots.txt)?$', 'django.views.static.serve', kwargs={'path': 'robots.txt', 'document_root': MEDIA_ROOT}),
)

# handler404 = views.error404
# handler500 = views.error500

