from rest_framework import serializers
from .models import *
from Users.models import *
from Users.serializers import *


class CreateContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        exclude = ['Tags']
        # fields = '__all__'

class ContactsSerializer(serializers.ModelSerializer):
    # this method is used to return name only insted of object
    Tags = serializers.SerializerMethodField()
    def get_Tags(self, obj):
        return [tag.Name for tag in obj.Tags.all()]
    
    # this method is used to return id, name insted of object
    # User_Id = serializers.SerializerMethodField()
    # def get_User_Id(self, obj):
    #     return {'id': obj.User_Id.id, 'User_Name': obj.User_Id.User_Name}
        
    class Meta:
        model = Contacts
        fields = '__all__'
        # depth = 1

class RemarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remarks
        fields = '__all__'