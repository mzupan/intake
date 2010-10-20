from django.conf.urls.defaults import *

urlpatterns = patterns('admin.views',
    (r'^/?$', 'show_index'),
)
