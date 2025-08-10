from django import forms
from django.contrib.auth.models import User
# from .models import Report,Pathologist
from patient.models import Patient
from . import models


class PathologistUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PathologistForm(forms.ModelForm):
    class Meta:
        model=models.Pathologist
        fields=['address','mobile','status','profile_pic']






class ReportForm(forms.ModelForm):
    class Meta:
        model = models.Report
        fields = ['report_name','file']  # use actual field name

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        # Optional: filter only active patients
        # self.fields['report_id'].queryset = Patient.objects.filter(status=True)

