from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class User_address(models.Model):
    fullName = models.CharField(max_length=250,blank=True)
    mobileNumber = models.CharField(max_length=15,blank=True)
    pincode = models.CharField(max_length=10,blank=True)   
    streetAddress = models.CharField(max_length=250,blank=True)
    landmark = models.CharField(max_length=250,blank=True)
    city = models.CharField(max_length=250,blank=True)
    state = models.CharField(max_length=250,blank=True)
    country = models.CharField(max_length=200,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
     	return '{}'.format(self.mobileNumber)
