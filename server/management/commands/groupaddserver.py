import hashlib
import getpass
import sys

from django.core.management.base import BaseCommand

from server.models import ServerGroup, Server

class Command(BaseCommand):
    def _get_string(self, prompt, reader_func=raw_input):
        """Helper method to get a non-empty string.
        """
        string = ''
        while not string:
            string = reader_func(prompt + ': ')
        return string
    
    def handle(self, **kwargs):
        groups = ServerGroup.objects()

        i = 1
        for g in groups:
            print '%i) %s' % (i, g.name)
            i += 1

        num = self._get_string('Enter number to edit')
        
        g = groups[int(num)-1]
        
        print
        print "Editing %s now..." % g
        print 
        
        servers = Server.objects()
        
        i = 1
        for s in servers:
            print '%i) %s' % (i, s.host)
            i += 1
        
        num = self._get_string('Enter number to to add to the group')
        
        g.servers.append(servers[int(num)-1].id)
        g.save()