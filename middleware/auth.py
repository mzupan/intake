from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:

    def process_request(self, request):
        if not request.user.is_authenticated():
            path = request.path_info
            
            for m in EXEMPT_URLS:
                if m.match(path):
                    return
                
            return HttpResponseRedirect(settings.LOGIN_URL)
