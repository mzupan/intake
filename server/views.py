from django.shortcuts import render_to_response
from django.template import RequestContext

from server.models import ServerGroup, Server, Log

def show_index(request, group=False): 
    if group:
        #
        # getting the groups
        #
        groups = ServerGroup.objects()
        
        return render_to_response('server/index_group.html', {'groups': groups}, context_instance=RequestContext(request))
    else:
        #
        # getting all the servers
        #
        servers = Server.objects()

        return render_to_response('server/index.html', {'servers': servers}, context_instance=RequestContext(request))

def show_server(request, server=None):
    
    s = Server.objects(host=server).first()

    if request.GET.has_key('log'):
        #
        # grabbing the last 50 logs
        #
        logs = Log.objects(server=s, log=request.GET['log'])[:50]
        
        return render_to_response('server/log.html', {'server': s, 'logs': logs}, context_instance=RequestContext(request))

    
    return render_to_response('server/server.html', {'server': s}, context_instance=RequestContext(request))

def show_group(request, group=None):
    g = ServerGroup.objects(slug=group).first()
    
    if request.GET.has_key('log'):
        #
        # grabbing the last 50 logs
        #
        logs = Log.objects(server__in=g.servers, log=request.GET['log'])[:50]
        
        return render_to_response('server/log_group.html', {'group': g, 'logs': logs}, context_instance=RequestContext(request))

    return render_to_response('server/group.html', {'group': g}, context_instance=RequestContext(request))