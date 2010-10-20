from mongoengine import *

import datetime

class Server(Document):
    host = StringField()
    uuid = StringField()
    about = StringField()
    created = DateTimeField(default=datetime.datetime.now())
    modified = DateTimeField()
    logs = ListField(StringField())
    active = BooleanField(default=True)
    
    def __unicode__(self):
        return self.host
    
    def get_logs(self):
        logs = []

        if self.logs is not None:
            logs.extend(self.logs)
        
        for group in ServerGroup.objects(servers=self.id):
            if group.logs is not None:
                logs.extend(group.logs) 
        
        return list(set(logs))

class ServerGroup(Document):
    name = StringField()
    slug = StringField()
    about = StringField()
    created = DateTimeField(default=datetime.datetime.now())
    modified = DateTimeField()
    logs = ListField(StringField())
    group = ReferenceField('ServerGroup', required=False, default=None)
    servers = ListField(ObjectIdField())
    
    def __unicode__(self):
        return self.name
    
class Log(Document):
    server = ReferenceField(Server)
    created = DateTimeField(default=datetime.datetime.now())
    log = StringField()
    line = StringField()
