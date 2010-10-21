import hashlib
import getpass
import sys

from django.core.management.base import BaseCommand

from server.models import ServerGroup

class Command(BaseCommand):
    def _get_string(self, prompt, reader_func=raw_input, required=True):
        """Helper method to get a non-empty string.
        """
        string = ''
        while not string:
            string = reader_func(prompt + ': ')
            if not required:
                break
        return string.strip().strip()
    
    def handle(self, **kwargs):
        groups = ServerGroup.objects()

        i = 1
        for g in groups:
            print '%i) %s' % (i, g.name)
            i += 1

        num = self._get_string('Enter number to delete', required=False)
        
        groups[int(num)-1].delete()
        
        