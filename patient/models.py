from django.db import models

from django.db import models
from django.contrib.auth.models import User

from doctor.models import Doctor    # Assuming you have a Doctor model






class Patient(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"
    

class PrescriptionDetail(models.Model):
    # doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    medicines = models.TextField(help_text="Comma-separated medicine names")
    dosage_instructions = models.TextField()
    follow_up_date = models.DateField(null=True, blank=True)
    additional_notes = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f"Prescription for {self.patient} "
