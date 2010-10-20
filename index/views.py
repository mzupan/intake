from django.shortcuts import render_to_response
from django.template import RequestContext

def show_index(request): 

    return render_to_response('index/index.html', context_instance=RequestContext(request))
