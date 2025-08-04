from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import ReportForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from . import forms,views

from django.contrib.auth.decorators import login_required,user_passes_test


#for sinup doctor profile
def pathologist_signup_view(request):
    userForm=forms.PathologistUserForm()
    PathologistForm=forms.PathologistForm()
    mydict={'userForm':userForm,'pathologistForm':PathologistForm}
    if request.method=='POST':
        userForm=forms.PathologistUserForm(request.POST)
        PathologistForm=forms.PathologistForm(request.POST,request.FILES)
        if userForm.is_valid() and PathologistForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            Pathologist=PathologistForm.save(commit=False)
            Pathologist.user=user
            Pathologist=Pathologist.save()
            my_Pathologist_group = Group.objects.get_or_create(name='PATHOLOGIST') #Group the user belongs to that is doctor
            my_Pathologist_group[0].user_set.add(user)
        return HttpResponseRedirect('pathologistlogin')
    return render(request,'pathologist/pathologistsignup.html',context=mydict)




# Pathologist dashboard view
def is_pathologist(user):
    return user.groups.filter(name='PATHOLOGIST').exists()

@login_required(login_url=reverse_lazy('doctorlogin'))
@user_passes_test(is_pathologist)
def pathologist_dashboard_view(request):
    return render(request, 'pathologist/pathologist_dashboard.html')


# @login_required
def upload_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('report-success')
    else:
        form = ReportForm()
    return render(request, 'pathologist/upload_report.html', {'form': form})

def report_success(request):
    return render(request, 'pathologist/report_success.html')
