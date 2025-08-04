from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns =[
    path('patientsignup', views.patient_signup_view),
    path('patientlogin', LoginView.as_view(template_name='patient/patientlogin.html')),



#---------FOR PATIENT RELATED URLS AFTER LOGIN-------------------------------------
    path('patient-dashboard/', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment/', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment/', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment/', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-view-doctor/', views.patient_view_doctor_view,name='patient-view-doctor'),
    path('searchdoctor/', views.search_doctor_view,name='searchdoctor'),
    path('patient-discharge/', views.patient_discharge_view,name='patient-discharge'),

]