from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.urls import reverse_lazy
from . import forms,models
from hospital.models import Appointment,PatientDischargeDetails
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q # it is use for and or xor condition in query
from patient.models import Patient
from pathologist.models import Report
from patient.forms import PrescriptionDetailForm

# Create your views here.
#for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')


#for checking if user is doctor or not
def doctor_check(user):
    if user.groups.filter(name='Doctor').exists():
        return True 
    return False

     

#for sinup doctor profile
def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)  # ← Partially save Doctor info
            doctor.user = user                      # ← Link Doctor to User
            doctor.save()                           # ← Now save with ForeignKey set
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR') #Group the user belongs to that is doctor
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'doctor/doctorsignup.html',context=mydict)





#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists() 

@login_required(login_url=reverse_lazy('doctorlogin'))
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'doctor/doctor_dashboard.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'doctor/doctor_patient.html',context=mydict)





@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
     # add group_name for each patient (doctorId-patientId)
    for p in patients:
        p.group_name = f"{doctor.id}-{p.id}"
    return render(request,'doctor/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def view_patient_reports(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    reports = Report.objects.filter(report_id=patient).order_by('-uploaded_at')

    return render(request, 'doctor/doctor_view_patient_reports.html', {
        'patient': patient,
        'reports': reports,
        'doctor':doctor
    })


def doctor_prescription_view(request,pk):
    prescriptionForm = PrescriptionDetailForm()
    patient = get_object_or_404(Patient, id=pk)
    if request.method == 'POST':
        prescriptionForm = PrescriptionDetailForm(request.POST)
        if prescriptionForm.is_valid():
            prescription = prescriptionForm.save(commit=False)
            prescription.patient = patient
            # prescription.doctor = models.Doctor.objects.get(user_id=request.user.id)
            prescription.save()
            return redirect('doctor-view-patient')
        
    return render(request, 'doctor/doctor_prescription.html', {
        'prescriptionForm': prescriptionForm,
        'patient': patient,
        'doctor': models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    })



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def search_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'doctor/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'doctor/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'doctor/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'doctor/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'doctor/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'doctor/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#--------------------------------------------------------------

