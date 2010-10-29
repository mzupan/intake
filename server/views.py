from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

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
        if request.method == "POST":
            #
            # grabbing the last 50 logs from our search string
            #
            logs = Log.objects(server=s, log=request.GET['log'], line__icontains=request.POST['search']).limit(50)
        else:
            #
            # grabbing the last 50 logs
            #
            logs = Log.objects(server=s, log=request.GET['log']).limit(50)
        
        log = ""
        for l in logs:
            log += l.line
            
        return render_to_response('server/log.html', {'server': s, 'log': log}, context_instance=RequestContext(request))

    
    return render_to_response('server/server.html', {'server': s}, context_instance=RequestContext(request))

def show_group(request, group=None):
    g = ServerGroup.objects(slug=group).first()
    
    if request.GET.has_key('log'):
        out = []
        line = ""
        
        if request.method == "POST":
            #
            # grabbing the last 50 logs from our search string
            #
            logs = Log.objects(server__in=g.servers, log=request.GET['log'], line__icontains=request.POST['search']).limit(50)
        else:
            #
            # grabbing the last 50 logs
            #
            logs = Log.objects(server__in=g.servers, log=request.GET['log']).limit(50)
        
        if logs.count() > 0:
            old = logs[0]
            for l in logs:
                if old.server == l.server:
                    line += l.line
                else:
                    if old is not None:
                        out.append({'server': old.server, 'line': line})
                    
                    old = l
                    line = l.line

        #
        # append the last line
        #
        if line != "":
            out.append({'server': old.server, 'line': line})
            
        return render_to_response('server/log_group.html', {'group': g, 'logs': out}, context_instance=RequestContext(request))

    return render_to_response('server/group.html', {'group': g}, context_instance=RequestContext(request))

@csrf_exempt
def ajax_get_latest(request):
    return HttpResponse("1")