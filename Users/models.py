from django.db import models

import uuid
# Create your models here.
class Users(models.Model):
    # Field to store the unique identifier
    Unique_Id           = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    User_Name           = models.CharField(max_length = 250, blank=True, default = '')
    Country_Code        = models.CharField(max_length = 250, blank=True, default = '')
    Phone_No            = models.CharField(max_length = 250, blank=True, null=False)
    Email_Id            = models.CharField(max_length = 250, blank=True, default = '')
    Company_Name        = models.CharField(max_length = 250, blank=True, default = '')
    Designation_Name    = models.CharField(max_length = 250, blank=True, default = '')
    Address             = models.CharField(max_length = 250, blank=True, default = '')
    Website_url         = models.CharField(max_length = 250, blank=True, default = '')
    Linkdin_url         = models.CharField(max_length = 250, blank=True, default = '')
    Notes               = models.TextField(blank=True, default = '')
    Profile_pic         = models.CharField(max_length = 250, blank=True, default = '')
    Created_at          = models.DateTimeField(auto_now_add=True)
    Updated_at          = models.DateTimeField(auto_now=True)
    OTP                 = models.IntegerField(blank=True, null=True)