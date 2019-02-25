from django.conf.urls import include, url, handler400, handler403, handler404, handler500
from django.contrib import admin
from django.views.generic import RedirectView
from django.views.static import serve

from adminplus.sites import AdminSitePlus
from filemanager import path_end

from src.settings import MEDIA_ROOT, DEBUG, IS_MAINTENANCE, env
from src import views
from src import user

admin.site = AdminSitePlus()
admin.site.index_title = '%s Administration' % env('SERVER_NAME')
admin.autodiscover()
admin.site.login = user.user_login
admin.site.logout = user.user_logout


if IS_MAINTENANCE:
    urlpatterns = [
        url(r'^ping_test/?$', views.ping_test),
        url(r'^get_staff/?$', views.get_staff),

        url(r'^site_media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT + '/media'}),
        url(r'^robots.txt$', serve, kwargs={'path': 'robots.txt', 'document_root': MEDIA_ROOT}),

        url(r'^$', views.error503),
        url(r'^.*/?$', RedirectView.as_view(url='/', permanent=True)),
    ]
else:
    urlpatterns = [
        url(r'^$', views.index),
        url(r'^(research|news|people|publications|resources|contact)/?$', views.pages),

        url(r'^(index\.html|home|index)/?$', RedirectView.as_view(url='/', permanent=True)),
        url(r'^(das_research\.html|science)/?$', RedirectView.as_view(url='/research/', permanent=True)),
        url(r'^(das_news\.html|activity)/?$', RedirectView.as_view(url='/news/', permanent=True)),
        url(r'^(das_people\.html|member|members)/?$', RedirectView.as_view(url='/people/', permanent=True)),
        url(r'^(das_publications\.html|publication|pub)/?$', RedirectView.as_view(url='/publications/', permanent=True)),
        url(r'^(das_resources\.html|resource)/?$', RedirectView.as_view(url='/resources/', permanent=True)),
        url(r'^(das_contact\.html|contacts)/?$', RedirectView.as_view(url='/contact/', permanent=True)),
        url(r'^groups/?$', RedirectView.as_view(url='/group/', permanent=True)),
        url(r'^admin$', RedirectView.as_view(url='/admin/', permanent=True)),

        url(r'^signin/?$', user.user_login),
        url(r'^signout/?$', user.user_logout),
        url(r'^password/?$', user.user_password),
        url(r'^get_staff/?$', views.get_staff),

        url(r'^group/?$', views.group_index),
        url(r'^group/dash/(?P<keyword>.*)/?$', views.group_dash),
        url(r'^group/archive/upload/?$', user.user_upload),
        url(r'^group/email_admin/?$', user.user_email),
        url(r'^group/(?P<path>.*)/?$', views.group_pages),

        url(r'^ping_test/?$', views.ping_test),
        url(r'^site_media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT + '/media'}),
        url(r'^site_data/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT + '/data'}),

        url(r'^error/400/?$', views.error400),
        url(r'^error/401/?$', views.error401),
        url(r'^error/403/?$', views.error403),
        url(r'^error/404/?$', views.error404),
        url(r'^error/500/?$', views.error500),
        url(r'^error/503/?$', views.error503),

        url(r'^admin/browse/' + path_end, user.browse),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^robots.txt$', serve, kwargs={'path': 'robots.txt', 'document_root': MEDIA_ROOT}),
    ]

    if DEBUG:
        urlpatterns.append(url(r'^test/?$', views.test))

handler400 = views.error400
handler403 = views.error403
handler404 = views.error404
handler500 = views.error500

