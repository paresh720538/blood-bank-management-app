from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels
from hospital.models import hospitalRegister
import random
from patient.models import allrequestinfo


def donor_signup_view(request):
    userForm=forms.DonorUserForm()
    donorForm=forms.DonorForm()
    print(userForm,donorForm)
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=forms.DonorUserForm(request.POST)
        donorForm=forms.DonorForm(request.POST,request.FILES)
        print(donorForm.is_valid(),'donor','**************************************')
        print(userForm.is_valid(),'user','**************************************')
        if  userForm.is_valid() and  donorForm.is_valid():
            print('it is working------------------------------------------------')
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            my_donor_group = Group.objects.get_or_create(name='DONOR')
            my_donor_group[0].user_set.add(user)
        return HttpResponseRedirect('donorlogin')
    return render(request,'donor/donorsignup.html',context=mydict)



def donor_dashboard_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Rejected').count(),
    }
    return render(request,'donor/donor_dashboard.html',context=dict)


def donate_blood_view(request):
    donation_form=forms.DonationForm()
    if request.method=='POST':
        donation_form=forms.DonationForm(request.POST)
        if donation_form.is_valid():
            blood_donate=donation_form.save(commit=False)
            blood_donate.bloodgroup=donation_form.cleaned_data['bloodgroup']
            donor= models.Donor.objects.get(user_id=request.user.id)
            blood_donate.donor=donor
            blood_donate.save()
            email = request.POST['email']
            pincode = request.POST['pincode']
            paddress = hospitalRegister.objects.filter(pincode = pincode).first()
            body = paddress.address
            hname = paddress.username
            random_number = random.randint(10000, 99999)
            allrequestinfo.objects.create(email = email,random_number = random_number,cetagory = 'donor')
            subject = "Your Request id  : "+ str(random_number) +"\n"+ " Venue- " + hname +" , "+body+" , "+pincode+" ,Thank You!"
            send_mail(
            'Your Slot has been booked Successfully for donating - Life Line Savior',
            subject,
            'settings.EMAIL_HOST_USER', 
            [email], 
            fail_silently=False
        )
            return HttpResponseRedirect('donation-history')  
    return render(request,'donor/donate_blood.html',{'donation_form':donation_form})

def donation_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    donations=models.BloodDonate.objects.all().filter(donor=donor)
    return render(request,'donor/donation_history.html',{'donations':donations})

def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            donor= models.Donor.objects.get(user_id=request.user.id)
            blood_request.request_by_donor=donor
            blood_request.save()
            email = request.POST['email']
            pincode = request.POST['pincode']
            paddress = hospitalRegister.objects.filter(pincode = pincode).first()
            body = paddress.address
            hname = paddress.username
            random_number = random.randint(10000, 99999)
            allrequestinfo.objects.create(email = email,random_number = random_number,cetagory = 'reciever')
            message = "Your Blood Request has been sent successfully, Your Request id  : "+str(random_number) +"\n"+ " Recieve Your Blood form - "+ hname +" ,"+body+" ,"+pincode+ " ,Thank you 👍"
            print(email)
            send_mail(
            'Request has been sent successfully to Life Line Savior',
            message,
            'settings.EMAIL_HOST_USER', 
            [email], 
            fail_silently=False
        )
            return HttpResponseRedirect('request-history')  
    return render(request,'donor/makerequest.html',{'request_form':request_form})

def request_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_donor=donor)
    return render(request,'donor/request_history.html',{'blood_request':blood_request})

