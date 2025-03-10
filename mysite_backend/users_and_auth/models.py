from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
