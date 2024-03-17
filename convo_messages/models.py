from django.db import models
# from django.contrib.postgres.fields impor
from convos.models import Convos
# Create your models here.

class ConvoMessages(models.Model):
    class TypeEnum(models.TextChoices):
        USER = 'user', 'User'
        SYSTEM = 'system', 'System'

    convo = models.ForeignKey(Convos, on_delete = models.CASCADE, blank = False, null = False)
    body = models.TextField()
    type = models.CharField(choices = TypeEnum.choices, null = False)
    created_at = models.DateTimeField(auto_now_add = True)    
    deleted = models.BooleanField()

    def delete(self, keep_parents=True):
        self.deleted = True
        self.save(keep_parents=keep_parents)
