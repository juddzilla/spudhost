from django.db import models
from django.contrib.auth.models import User
import uuid

class Quick_Queue(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    body = models.TextField()        
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)    
    deleted = models.BooleanField(default=False)

    def delete(self):
        self.deleted = True
        self.save()