from django.contrib import admin

# Register your models here.

from .models import PasswordRecord

admin.site.register(PasswordRecord)

