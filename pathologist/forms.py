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
        fields = ['patient', 'report_name', 'file']

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        # Filter only active patients (status=True)
        self.fields['patient'].queryset = Patient.objects.filter(status=True)
