from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Mediatheque(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Animation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    hour = models.TimeField()
    hour_end = models.TimeField()
    age = models.IntegerField()
    age_end = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/')
    nb_places = models.IntegerField()
    users = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animation = models.ForeignKey(Animation, on_delete=models.CASCADE)
    Validated = models.BooleanField(default=False)
    nb_person = models.IntegerField(default=1)
    mediatheque = models.ForeignKey(Mediatheque, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


