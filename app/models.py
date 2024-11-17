from django.db import models
import os
# Create your models here.
class UsersModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=100)
    contact = models.IntegerField()
    address = models.CharField(max_length=100)
    profile = models.FileField(upload_to=os.path.join('static', 'userprofiles'))
    otp = models.IntegerField(null=True)
    
    

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "UsersModel"


class TechnicianModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=100)
    contact = models.IntegerField()
    address = models.CharField(max_length=100)
    amount = models.IntegerField()
    techrole = models.CharField(max_length=100)
    profile = models.FileField(upload_to=os.path.join('static', 'Techprofiles'))
    status=models.CharField(max_length=100,default='pending')
    otp = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "TechnicianModel"

class ServiceBookingModel(models.Model):
    sid=models.IntegerField()
    username = models.CharField(max_length=100)
    useremail = models.CharField(max_length=100)
    techemail = models.CharField(max_length=100)
    contact = models.IntegerField()
    address = models.CharField(max_length=100)
    amount = models.IntegerField()
    techrole = models.CharField(max_length=100)
    profile = models.FileField(upload_to=os.path.join('static', 'Bookedprofiles'))
    status=models.CharField(max_length=100,default='pending')
    feedback = models.TextField(default='None',null=True)

    def __str__(self):
        return self.username
    class Meta:
        db_table = "ServiceBookingModel"


class ContactUsModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        db_table = "ContactUsModel"