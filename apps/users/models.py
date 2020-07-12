from django.db import models


# Create your models here.
class User(models.Model):
    id = models.BigIntegerField(20, primary_key=True, unique=True)
    created_time = models.DateTimeField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    enable = models.BinaryField(1)
    last_update_time = models.DateTimeField()


class UserProfile(models.Model):
    address = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    work_place = models.CharField(max_length=255)
    last_update_time = models.DateTimeField()
    user_id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)


class Role(models.Model):
    id = models.BigIntegerField(20, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    last_update_time = models.DateTimeField()


class UserRole(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    last_update_time = models.IntegerField(11)

    class Meta:
        unique_together = (("user_id", "role_id"),)

