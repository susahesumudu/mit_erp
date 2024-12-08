from django.contrib import admin

# Register your models here.from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender')

admin.site.register(Profile, ProfileAdmin)

