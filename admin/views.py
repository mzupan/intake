from django.shortcuts import render_to_response
from django.template import RequestContext

def show_index(request, group=False): 
    return render_to_response('admin/index.html', context_instance=RequestContext(request))
