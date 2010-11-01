from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from django.utils.importlib import import_module

class InTakeSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        
        if request.path_info[0:5] == '/api/':
            engine = import_module(settings.SESSION_ENGINE)
            session_key = None
            request.session = engine.SessionStore(session_key)
        
        super(InTakeSessionMiddleware, self).process_request(request)

    def process_response(self, request, response):
        if request.path_info[0:5] == '/api/':
            return response
        
        super(InTakeSessionMiddleware, self).process_response(request, response)
        return response