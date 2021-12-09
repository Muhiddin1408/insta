from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female')
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, blank='m', max_length=64)
    followers = models.ManyToManyField('self', blank=True)
    following = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.username



