from django.contrib import admin
from .models import Image, Comment, LocationUser

admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(LocationUser)

