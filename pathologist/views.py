from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

from . import forms
from .forms import ReportForm
from patient.models import Patient


# ------------------------------
# Pathologist Signup View
# ------------------------------
def pathologist_signup_view(request):
    """
    Handles registration of a new Pathologist user.
    - Renders a signup form for both User and Pathologist profile.
    - Saves the new user and assigns them to the 'PATHOLOGIST' group.
    """
    userForm = forms.PathologistUserForm()
    PathologistForm = forms.PathologistForm()

    context = {
        'userForm': userForm,
        'pathologistForm': PathologistForm
    }

    if request.method == 'POST':
        userForm = forms.PathologistUserForm(request.POST)
        PathologistForm = forms.PathologistForm(request.POST, request.FILES)

        if userForm.is_valid() and PathologistForm.is_valid():
            # Save User
            user = userForm.save()
            user.set_password(user.password)  # hash the password
            user.save()

            # Save Pathologist profile linked to user
            pathologist = PathologistForm.save(commit=False)
            pathologist.user = user
            pathologist.save()

            # Add user to PATHOLOGIST group
            pathologist_group, created = Group.objects.get_or_create(name='PATHOLOGIST')
            pathologist_group.user_set.add(user)

            return HttpResponseRedirect('pathologistlogin')

    return render(request, 'pathologist/pathologistsignup.html', context)


# ------------------------------
# Helper: Check if user is Pathologist
# ------------------------------
def is_pathologist(user):
    """Returns True if the user belongs to the PATHOLOGIST group."""
    return user.groups.filter(name='PATHOLOGIST').exists()


# ------------------------------
# Pathologist Dashboard View
# ------------------------------
@login_required(login_url=reverse_lazy('doctorlogin'))
@user_passes_test(is_pathologist)
def pathologist_dashboard_view(request):
    """
    Displays the Pathologist dashboard:
    - Shows all patients (with search functionality).
    - Allows filtering patients by name, ID, or mobile number.
    """
    search_query = request.GET.get('search', '')

    # Get all patients
    total_patient = Patient.objects.all()
    patient_count = total_patient.count()

    # Apply search filter if query is provided
    if search_query:
        total_patient = total_patient.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(id__icontains=search_query) |
            Q(mobile__icontains=search_query)
        )

    return render(request, 'pathologist/pathologist_dashboard.html', {
        'total_patient': total_patient,
        'patient_count': patient_count,
    })


# ------------------------------
# Upload Report View
# ------------------------------
@login_required
@user_passes_test(is_pathologist)
def upload_report(request, pk):
    """
    Allows Pathologist to upload a report for a specific patient.
    - Patient is identified by the primary key (pk) in URL.
    - Saves report with a link to the patient.
    """
    patient = get_object_or_404(Patient, id=pk)

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            # Create report object but don't save to DB yet
            report = form.save(commit=False)
            report.report_id = patient  # Link report to patient
            report.save()
            return redirect('report-success')
    else:
        form = ReportForm()

    return render(request, 'pathologist/upload_report.html', {
        'form': form,
        'patient_id': patient.id,
        'patient_name': patient.get_name,
    })


# ------------------------------
# Report Success Page
# ------------------------------
def report_success(request):
    """
    Displays a simple confirmation page after a report is uploaded successfully.
    """
    return render(request, 'pathologist/report_success.html')
