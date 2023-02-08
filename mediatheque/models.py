from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Mediatheque(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Animation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    hour = models.TimeField()
    age = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    mediatheque = models.ForeignKey(Mediatheque, on_delete=models.CASCADE)

    def __str__(self):
        return self.name