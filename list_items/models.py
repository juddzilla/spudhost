from django.db import models
from lists.models import Lists

class ListItems(models.Model):    
    list = models.ForeignKey(Lists, on_delete = models.CASCADE, blank = False, null = False)
    order = models.IntegerField(default=0)
    body = models.TextField()   
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted = models.BooleanField(default=False)

    def delete(self, keep_parents=True):
        self.deleted = True
        self.save(keep_parents=keep_parents)

    # def __str__(self):
    #     return self.reason