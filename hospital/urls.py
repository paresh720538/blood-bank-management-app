from django.urls import path
from . import views


urlpatterns = [
    path("",views.registerHospital,name='hospital-register'),
    path('hospital-login',views.hospital_login,name='hospital-login'),
    path("fail-login",views.failure,name='fail-login'),
    path('hospital-dashboard',views.hospital_dashboard,name='hospital-dashboard'),
    path('h-success',views.hospital_success,name='h-success')
    
]