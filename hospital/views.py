from django.shortcuts import render,redirect
from .forms import HospitalUserForm,HospitalLoginForm
from django.http import HttpResponse
from .models import hospitalRegister
# Create your views here.
def hospital_dashboard(request):    
    return render(request, 'hospital/hospitalbase.html')


def  registerHospital(request):
    if request.method == 'POST':
        hospital_form = HospitalUserForm(request.POST)
        print(request.POST)
        print(hospital_form.is_valid())
        if hospital_form.is_valid():
            hospital_form.save()
        return redirect('hospital-login')
    hospital_form = HospitalUserForm()
    return render(request,'hospital/hospitalregister.html',{'form2':hospital_form})


def hospital_login(request):
    print(request.method)
    if request.method == 'POST':
            formlogin = HospitalLoginForm(request, data=request.POST)
            print('working.........................')
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username,password)
            d = hospitalRegister.objects.filter(username = username).first()
           
            
            if (d):
                if d.status == 'approved' and d.password == password:
                    return redirect('h-success')
            else:
                formlogin = HospitalLoginForm()
                return render(request,'hospital/hospitallogin.html',{'message':'Sorry Your Request is not approved.','formlogin':formlogin})
            return redirect('fail-login')
    formlogin = HospitalLoginForm()
    return render(request,'hospital/hospitallogin.html',{'formlogin':formlogin})



def failure(request):
    return render(request,'hospital/failure.html')


def hospital_success(request):
    return render(request,'hospital/hospital_success.html')