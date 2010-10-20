from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms

import simplejson

from server.models import Server, ServerGroup, Log

@csrf_exempt
def do_api(request):
    if request.method == "POST":
        try:
            if request.POST['action'] == "add":
                do_add(request)
        except Exception, err:
            s = do_verify(request)
            
            if s.active:
                return send_logs(s)
            
    return HttpResponse("")

def do_verify(request):
    #
    # getting if the uuid is assigned to a server.. if not create it
    #
    s = Server.objects(uuid=request.POST['server']).first()
    if s is None:
        s = Server(host=request.POST['host'], uuid=request.POST['server'])
        s.save()
        
    return s
    
def send_logs(s):
    #
    # send the logs back to the server that needs to be sent over
    #
    logs = []
    
    #
    # getting all logs for the server
    #
    if s.logs is not None:
        logs.extend(s.logs)
    
    #
    # does the server have a group?
    #
    for group in ServerGroup.objects(servers=s.id):
        if group.logs is not None:
            logs.extend(group.logs) 
    
    #
    # remove the dups
    #
    logs = list(set(logs))

    return HttpResponse(simplejson.dumps(logs))

def do_add(request):
    #
    # find the server
    #
    s = Server.objects(uuid=request.POST['server']).first()
    
    #
    # add the log
    #
    j = simplejson.loads(request.POST['log'])
    
    #
    # formatting the log
    #
    log = ""
    for l in j['line']:
        log += l.strip() + "\n"

    l = Log(server=s, log=j['log'], line=log)
    l.save()
    