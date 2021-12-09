from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class UserAdminForm(UserAdmin):
    class Meta:
        model = User
        fields = ['id', ]


admin.site.register(User, UserAdminForm)
