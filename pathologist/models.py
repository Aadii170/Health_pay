from django.db import models
from django.contrib.auth.models import User
from patient.models import Patient  # Import existing Patient model


class Pathologist(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PathologistProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    status=models.BooleanField(default=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.user.last_name)
        



class Report(models.Model):
    report_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    report_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_name} - {self.report_id}"  # report_id gives Patient object

