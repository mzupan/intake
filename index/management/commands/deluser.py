from django.core.management.base import BaseCommand

from mongoengine.django.auth import User


class Command(BaseCommand):

    def _get_string(self, prompt, reader_func=raw_input):
        """Helper method to get a non-empty string.
        """
        string = ''
        while not string:
            string = reader_func(prompt + ': ')
        return string
    
    def handle(self, **kwargs):
        username = self._get_string('Username')
        user = User.objects(username=username).first()
        if user:
            user.delete()
            print 'User "%s" successfully removed' % (username)
        else:
            print 'Error! Could not find user with username "%s"' % username