from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    slug = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='slug', db_index=True)
    email = models.EmailField(_("email address"), unique=True, null=False, blank=False)

    class Meta:
        db_table = "auth_user"