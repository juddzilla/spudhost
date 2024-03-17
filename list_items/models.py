from django.db import models
from lists.models import Lists

class ListItems(models.Model):    
    list = models.ForeignKey(Lists, on_delete = models.CASCADE, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    body = models.TextField()   
    completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now = True)
    deleted = models.BooleanField(default=False)

    def delete(self, keep_parents=True):
        self.deleted = True
        self.save(keep_parents=keep_parents)

    # def __str__(self):
    #     return self.reason