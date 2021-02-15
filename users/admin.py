from django.contrib import admin
from .models import CustomUser
from .forms import UserAdmin
from django.contrib.auth.models import Group


admin.site.register(CustomUser, UserAdmin)

admin.site.unregister(Group)