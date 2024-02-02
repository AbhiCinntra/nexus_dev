import uuid
from django.db import models
from Users.models import Users

# Create your models here.
class Cards(models.Model):
    Unique_Id           = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    User_Id             = models.ForeignKey(Users, on_delete=models.CASCADE)
    Country_Code        = models.CharField(max_length = 250, blank=True, default = '')
    Phone_No            = models.CharField(max_length = 250, blank=True, null=False)
    Card_Name           = models.CharField(max_length = 250, blank=True, default = '')
    User_Name           = models.CharField(max_length = 250, blank=True, default = '')
    Email_Id            = models.CharField(max_length = 250, blank=True, default = '')
    Company_Name        = models.CharField(max_length = 250, blank=True, default = '')
    Designation_Name    = models.CharField(max_length = 250, blank=True, default = '')
    Address             = models.CharField(max_length = 250, blank=True, default = '')
    Website_url         = models.CharField(max_length = 250, blank=True, default = '')
    Linkdin_url         = models.CharField(max_length = 250, blank=True, default = '')
    Notes               = models.TextField(blank=True, default = '')
    Profile_pic         = models.CharField(max_length = 250, blank=True, default = '')
    Default             = models.IntegerField(default=0)
    Created_at          = models.DateTimeField(auto_now_add=True)
    Updated_at          = models.DateTimeField(auto_now=True)