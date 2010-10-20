import hashlib
import getpass
import sys

from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

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
        return string

    def handle(self, **kwargs):
        while True:
            name = self._get_string('Group Name')
        
            if ServerGroup.objects(name=name).count() > 0:
                print "That group name is already in use"
                continue
            else:
                break

        g = ServerGroup(name=name)
        g.slug = slugify(g.name)
        g.save()

        print 'Server group "%s" successfully added' % (name)
