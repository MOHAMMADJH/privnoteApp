import datetime
import uuid

from django.db import models


# Create your models here.


class Note(models.Model):
    """
      class Note models field
    """
    note = models.TextField()
    key = models.CharField(max_length=250)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    date = models.IntegerField(default=0)
    self_d = models.DateField(default=datetime.date.today)
    note_name = models.CharField(max_length=100)
    is_d = models.BooleanField(default=False)
    note_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(), )

    def __str__(self):
        return str(self.note_id)
