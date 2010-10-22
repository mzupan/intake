import ldap

from mongoengine.django.auth import User
from django.conf import settings

class LDAPBackend:
    def authenticate(self, username=None, password=None, domain=None):
        base = settings.LDAP_BASE
        scope = ldap.SCOPE_SUBTREE
        filter = "(&(objectclass=person) (uid=%s))" % username
        ret = ['dn']

        try:
            l = ldap.initialize(settings.LDAP_SERVER);
            l.protocol_version = ldap.VERSION3
            l.simple_bind_s()
        except ldap.LDAPError:
            return None

        try:
            result_id = l.search(base, scope, filter, ret)
            result_type, result_data = l.result(result_id, 0)
            
            if (len(result_data) != 1):
                return None
            
            l.simple_bind_s(result_data[0][0],password)
            
            u = User.objects(username=username).first()
            if u is None:
                from random import choice
                import string
                temp_pass = ""
                for i in range(8):
                    temp_pass = temp_pass + choice(string.letters)

                u = User(username=username)
                u.email = username + settings.LDAP_EMAIL_DOMAIN
                u.set_password(temp_pass)
                u.is_staff = True
                u.is_superuser = False
                u.is_active = True
                u.save()

            return u
           
        except ldap.INVALID_CREDENTIALS:
            return None

    def get_user(self, user_id):
        try:
            return User.objects(id=user_id).first()
        except:
            return None
