from django.conf.urls.defaults import *

urlpatterns = patterns('server.views',
    (r'^/?$', 'show_index'),
    (r'^(?P<server>.+)/$', 'show_server'),
    (r'^ajax/getlatest/$', 'ajax_get_latest'),
)
