from django.conf.urls.defaults import *

urlpatterns = patterns('api.views',
    (r'^/?$', 'do_api'),
)