import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.timezone import now

class User(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name='core_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='core_user_permissions', blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    app_secret_token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)

class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='destinations')
    url = models.URLField()
    http_method = models.CharField(max_length=10, choices=[('GET', 'GET'), ('POST', 'POST')])
    headers = models.JSONField()

class Log(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='logs')
    received_timestamp = models.DateTimeField(default=now)
    processed_timestamp = models.DateTimeField(null=True, blank=True)
    received_data = models.JSONField()
    status = models.CharField(max_length=10, choices=[('success', 'Success'), ('failed', 'Failed')])
