from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^api/', include('api.urls')),
    (r'^server/', include('server.urls')),
    (r'^group/', include('server.urls_group')),
    (r'^admin/', include('admin.urls')),
    
    
    (r'^/?$', 'index.views.show_index'),
    
    #
    # login/logout
    #
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'index/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login/?logout=1'}),
)


#
# handling static pages for development only
#
from django.conf import settings
if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"%s(?P<path>.*)/$" % settings.MEDIA_URL[1:], "static.serve", {
            "document_root": settings.MEDIA_ROOT,
        })
    )
