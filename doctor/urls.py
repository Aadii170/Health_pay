from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('doctorsignup', views.doctor_signup_view,name='doctorsignup'),
    path('doctorlogin/', LoginView.as_view(template_name='doctor/doctorlogin.html'), name='doctorlogin'),


    #----------------- after login doctors urls--------------------------------------
    path('doctor-dashboard/', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('search', views.search_view,name='search'),

    path('doctor-patient/', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient/', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('view-patient-reports/<int:patient_id>/', views.view_patient_reports, name='view_patient_reports'),
    path('doctor-prescription/<int:pk>/', views.doctor_prescription_view, name='doctor-prescription'),

    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    path('doctor-appointments/', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
  
]
