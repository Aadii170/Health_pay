from django.contrib import admin
from .models import Doctor
# Register your models here.
@admin.register(Doctor)
class Doctoradmin(admin.ModelAdmin):
    list_display=['id', 'get_name', 'department', 'mobile', 'status']