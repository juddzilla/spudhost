from django.db import models
from django.contrib.auth.models import User
import uuid

class Convos(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.TextField()        
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted = models.BooleanField(default=False)

    def delete(self, keep_parents=True):
        self.deleted = True
        self.save(keep_parents=keep_parents)
