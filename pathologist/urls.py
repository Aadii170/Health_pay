from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

# URL patterns for pathologist app
urlpatterns = [
    path('pathologistsignup', views.pathologist_signup_view,name='pathologistsignup'),
    path('pathologistlogin/', LoginView.as_view(template_name='pathologist/pathologistlogin.html'), name='doctorlogin'),
    path('pathologist-dashboard/', views.pathologist_dashboard_view, name='pathologist-dashboard'),


    path('upload/<int:pk>/', views.upload_report, name='upload-report'),
    path('success/', views.report_success, name='report-success'),
]
