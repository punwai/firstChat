from django.contrib import admin
from .models import Room

# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    pass
admin.site.register(Room, RoomAdmin)
