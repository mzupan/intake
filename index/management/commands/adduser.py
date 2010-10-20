import hashlib
import getpass
import sys

from django.core.management.base import BaseCommand

from mongoengine.django.auth import User


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
            username = self._get_string('Username')
        
            if User.objects(username=username).count() > 0:
                print "That username is already in use"
                continue
            else:
                break
        
        while True:
            email = self._get_string('Email', required=False)
        
            if User.objects(email=email).count() > 0:
                print "That email is already in use"
                continue
            else:
                break
            
        password = self._get_string('Password', getpass.getpass)
        first_name = self._get_string('First name')
        last_name = self._get_string('Last name')

        u = User(username=username)
        u.first_name = first_name
        u.last_name = last_name
        u.email = email
        u.set_password(password)
        u.is_staff = True
        u.is_superuser = False
        u.save()

        print 'User "%s %s" successfully added' % (first_name, last_name)
