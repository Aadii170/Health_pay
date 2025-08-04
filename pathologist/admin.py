from django.contrib import admin
from .models import Report,Pathologist
 
@admin.register(Pathologist)
class Pthologistadmin(admin.ModelAdmin):
    list_display=['id', 'get_name', 'mobile', 'status']


admin.site.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_name', 'patient', 'uploaded_at')
    search_fields = ('report_name', 'patient__name')
