from django.contrib import admin

# Register your models here.
from .models import users, logging

admin.site.register(users)
admin.site.register(logging)
