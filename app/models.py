import django
from django.db import models
from django.contrib.auth.hashers import make_password


# Create your models here.


class users(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.password = make_password(password=self.password, salt='salt', hasher='md5')
        super(users, self).save(*args, **kwargs)


class logging(models.Model):
    timestamp = models.DateTimeField(default=django.utils.timezone.now)
    user = models.CharField(max_length=20)
    attempt_count = models.IntegerField(default=0)
    result = models.CharField(max_length=20)
