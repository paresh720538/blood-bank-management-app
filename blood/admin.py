from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Stock)
admin.site.register(models.BloodRequest)
admin.site.register(models.contact)