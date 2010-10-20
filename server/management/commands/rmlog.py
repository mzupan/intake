import hashlib
import getpass
import sys

from django.core.management.base import BaseCommand
from optparse import make_option

from server.models import ServerGroup, Server, Log

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--server', '-s', dest='server', help='Delete a log to a server', default=False, action='store_true'),
        make_option('--group', '-g', dest='group', help='Delete a log to a group', default=False, action='store_true'),
    )
    
    def _get_string(self, prompt, reader_func=raw_input, required=True):
        """Helper method to get a non-empty string.
        """
        string = ''
        while not string:
            string = reader_func(prompt + ': ')
            if not required:
                break
        return string
    
    def handle(self, **kwargs):
        if kwargs['server']:
            servers = Server.objects()
            
            i = 1
            for s in servers:
                print '%i) %s' % (i, s.host)
                i += 1
    
            num = self._get_string('Enter number to add to')
            
            obj = servers[int(num)-1]
        
        if kwargs['group']:
            groups = ServerGroup.objects()
    
            i = 1
            for g in groups:
                print '%i) %s' % (i, g.name)
                i += 1
    
            num = self._get_string('Enter number to add to')
        
            obj = groups[int(num)-1]


        while True:
            #
            # list the logs for the server/group now
            #
            if len(obj.logs) == 0:
                break
            
            i = 1
            for l in obj.logs:
                print '%i) %s' % (i, l)
                i += 1
                
            num = int(self._get_string('Enter number to delete'))
            if num > 0:
                obj.logs.pop(num-1)
                obj.save()
            