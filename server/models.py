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
    
    meta = {
        'ordering': ['+host']
    }
    
    def __unicode__(self):
        return self.host
    
    def get_logs(self):
        logs = []

        if self.logs is not None:
            logs.extend(self.logs)
        
        for group in ServerGroup.objects(servers=self.id):
            if group.logs is not None:
                logs.extend(group.logs) 
        
        list(set(logs))
        logs.sort()

        return logs

class ServerGroup(Document):
    name = StringField()
    slug = StringField()
    about = StringField()
    created = DateTimeField(default=datetime.datetime.now())
    modified = DateTimeField()
    logs = ListField(StringField())
    group = ReferenceField('ServerGroup', required=False, default=None)
    servers = ListField(ObjectIdField())
    
    meta = {
        'ordering': ['+name']
    }
    
    def __unicode__(self):
        return self.name
    
    def get_logs(self):
        logs = self.logs
        
        list(set(logs))
        logs.sort()

        return logs
    
    def get_servers(self):
        return Server.objects(id__in=self.servers)
    
    def get_log_count(self):
        return len(self.logs)
    
    def get_log_lines(self):
        return Log.objects(server__in=self.servers).count()
    
class Log(Document):
    server = ReferenceField(Server)
    created = DateTimeField(default=datetime.datetime.now())
    log = StringField()
    line = StringField()

    meta = {
        'ordering': ['-created'],
        'indexes': ['-created', 'log']
    }