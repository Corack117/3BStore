from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    slug = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='slug', db_index=True)

    class Meta:
        db_table = "auth_user"