from django.db import models
from Users.models import Users
import uuid
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create your models here.
class Tag(models.Model):
    Name                = models.CharField(max_length = 200, unique=True)
    Created_at          = models.DateTimeField(auto_now_add = True)
    Updated_at          = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.Name
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Contacts(models.Model):
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
    Tags                = models.ManyToManyField(Tag) # Tags = models.TextField(blank=True, default = '')
    Profile_pic         = models.CharField(max_length = 250, blank=True, default = '')
    Priority            = models.CharField(max_length = 250, blank=True, default = '')
    Favorite            = models.IntegerField(default = 0)
    Created_at          = models.DateTimeField(auto_now_add = True)
    Updated_at          = models.DateTimeField(auto_now = True)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Remarks(models.Model):
    Contact_Id          = models.ForeignKey(Contacts, on_delete=models.CASCADE)
    Messages            = models.TextField(blank = False, null= False)
    Created_at          = models.DateTimeField(auto_now_add = True)
    Updated_at          = models.DateTimeField(auto_now = True)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Followups(models.Model):
    User_Id             = models.ForeignKey(Users, on_delete=models.CASCADE)
    Contact_Id          = models.ForeignKey(Contacts, on_delete=models.CASCADE)
    Created_at          = models.DateTimeField(auto_now_add = True)
    Updated_at          = models.DateTimeField(auto_now = True)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>