from django.contrib import admin
from .models import Patient, PrescriptionDetail
# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'address', 'mobile', 'symptoms', 'assignedDoctorId', 'admitDate', 'status')

@admin.register(PrescriptionDetail)
class  PrescriptionDetailAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'diagnosis', 'medicines', 'dosage_instructions', 'follow_up_date', 'additional_notes')