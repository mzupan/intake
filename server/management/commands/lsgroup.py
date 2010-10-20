import hashlib
import getpass
import sys

from django.core.management.base import BaseCommand

from server.models import ServerGroup

class Command(BaseCommand):

    def handle(self, **kwargs):
        for g in ServerGroup.objects:
            print '%s (%s)' % (g.name, g.slug)
