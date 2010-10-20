from django.conf.urls.defaults import *

urlpatterns = patterns('server.views',
    (r'^/?$', 'show_index', {'group': True}),
    (r'^(?P<group>.+)/$', 'show_group'),
)
