from django.db import models
from account.models import User
from location_field.models.plain import PlainLocationField
from django.contrib.gis.geos import Point

# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='image')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class LocationUser(models.Model):
    city = models.CharField(max_length=100)
    location = PlainLocationField(based_fields=['city'], zoom=7)
