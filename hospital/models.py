from django.db import models

# Create your models here.
class hospitalRegister(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    hospital_registrationnumber = models.IntegerField()
    address = models.CharField(max_length=40,blank=True,null=True)
    pincode = models.IntegerField(blank=True,null=True)
    status=models.CharField(max_length=20,default="Pending")
    date=models.DateField(auto_now=True) 
    
    def __str__(self):
        return self.username