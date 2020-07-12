from django.db import models


# Create your models here.
class Setting(models.Model):
    setting_key = models.CharField(max_length=255, primary_key=True, unique=True)
    setting_value = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    editable = models.BinaryField(1)
    last_update_time = models.DateTimeField()


class DocumentTemplate(models.Model):
    type = models.CharField(max_length=255, primary_key=True, unique=True)
    content = models.TextField()
    description = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    last_update_time = models.DateTimeField()


class ErrorDescription(models.Model):
    code = models.CharField(max_length=255, primary_key=True, unique=True)
    description = models.CharField(max_length=255)
    last_update_time = models.DateTimeField()


class Info(models.Model):
    id = models.BigIntegerField(20, primary_key=True, unique=True)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    manual_guide = models.CharField(max_length=255)
    last_update_time = models.DateTimeField()


class SystemMessage(models.Model):
    system_message_id = models.BigIntegerField(20)
    content = models.CharField(max_length=255)
    last_update_time = models.DateTimeField()
