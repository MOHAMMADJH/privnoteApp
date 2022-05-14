import datetime
import uuid

from django.db import models


# Create your models here.


class Note(models.Model):
    """
      class Note models field
    """
    note_id = models.UUIDField(default=uuid.uuid4, editable=False)
    note = models.TextField()
    # key = models.CharField(max_length=250, blank=True, )
    email = models.EmailField(null=True, max_length=200, blank=True)
    password = models.CharField(null=True, max_length=200, blank=True)
    date = models.DateField(null=True, auto_now_add=True)
    self_d = models.DateField(null=True, blank=True)
    note_name = models.CharField(null=True, max_length=100, blank=True)
    is_d = models.BooleanField(null=True, default=False)

    def __str__(self):
        return str(self.note_id)

