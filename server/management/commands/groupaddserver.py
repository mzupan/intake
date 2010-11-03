import hashlib
import getpass
import sys

from django.core.management.base import BaseCommand

from server.models import ServerGroup, Server

class Command(BaseCommand):
    def _get_string(self, prompt, reader_func=raw_input, required=True):
        """Helper method to get a non-empty string.
        """
        string = ''
        while not string:
            string = reader_func(prompt + ': ')
            
            if string == "q":
                sys.exit()
            
            if not required:
                break
        return string.strip()
    
    def handle(self, **kwargs):
        groups = ServerGroup.objects().order_by('name')

        i = 1
        for g in groups:
            print '%i) %s' % (i, g.name)
            i += 1
        
        print 'q) Quit'

        num = self._get_string('Enter number to edit')
        
        g = groups[int(num)-1]

        print
        print "Editing %s now..." % g
        print 
        
        servers = []

        i = 1
        for s in Server.objects().order_by('name'):
            if s.id not in g.servers:
                print '%i) %s' % (i, s.host)
                i += 1l;s
                servers.append(s)
            
        num = self._get_string('Enter number to to add to the group')
        
        g.servers.append(servers[int(num)-1].id)
        g.save()
