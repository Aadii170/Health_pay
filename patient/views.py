from django.shortcuts import render,redirect,reverse

from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from doctor.models import Doctor
from doctor.forms import DoctorForm,DoctorUserForm
from . import forms,models
from patient.models import Patient, PrescriptionDetail
from hospital.models import Appointment,PatientDischargeDetails
from hospital.forms import AppointmentForm,PatientAppointmentForm
from pathologist.models import Report

# Create your views here.



#for showing signup/login button for doctor(by sumit)
def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'patient/patientsignup.html',context=mydict)





#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=Patient.objects.get(user_id=request.user.id)
    doctor=Doctor.objects.get(user_id=patient.assignedDoctorId)
    report= Report.objects.filter(report_id=patient.id) # Get the latest report for the patient
    group_name = f"{doctor.id}-{patient.id}" # Unique group name for patient-doctor chat
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'group_name':group_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    'total_reports': report,
    }
    return render(request,'patient/patient_dashboard.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    doctor=Doctor.objects.get(user_id=patient.assignedDoctorId)
    group_name = f"{doctor.id}-{patient.id}"
    return render(request,'patient/patient_appointment.html',{'patient':patient,'group_name':group_name})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=PatientAppointmentForm()
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    doctor=Doctor.objects.get(user_id=patient.assignedDoctorId)
    group_name = f"{doctor.id}-{patient.id}"
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message,'group_name':group_name}
    if request.method=='POST':
        appointmentForm=PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('/patient/patient-view-appointment')
    return render(request,'patient/patient_book_appointment.html',context=mydict)



def patient_view_doctor_view(request):
    doctors=Doctor.objects.all().filter(status=True)

    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    doctor=Doctor.objects.get(user_id=patient.assignedDoctorId)
    group_name = f"{doctor.id}-{patient.id}"
    return render(request,'patient/patient_view_doctor.html',{'patient':patient,'doctors':doctors,'group_name':group_name})



def search_doctor_view(request):
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors=Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    doctor=Doctor.objects.get(user_id=patient.assignedDoctorId)
    group_name = f"{doctor.id}-{patient.id}"
    return render(request,'patient/patient_view_doctor.html',{'patient':patient,'doctors':doctors,'group_name':group_name})




@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=Appointment.objects.all().filter(patientId=request.user.id)
    doctor=Doctor.objects.get(user_id=patient.assignedDoctorId)
    group_name = f"{doctor.id}-{patient.id}"
    return render(request,'patient/patient_view_appointment.html',{'appointments':appointments,'patient':patient,'group_name':group_name})

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_prescription_view(request):
    patient=Patient.objects.get(user_id=request.user.id)
    prescription= PrescriptionDetail.objects.filter(patient__user_id=request.user.id).order_by('-date')
    doctor=Doctor.objects.get(user_id=patient.assignedDoctorId)
    group_name = f"{doctor.id}-{patient.id}"
    return render(request, 'patient/patient_view_prescription.html', {'prescriptions': prescription, 'patient': patient,'group_name':group_name})




@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    doctor=Doctor.objects.get(user_id=patient.assignedDoctorId)
    group_name = f"{doctor.id}-{patient.id}"
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'group_name':group_name,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'group_name':group_name,
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'patient/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------


