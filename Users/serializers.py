from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class UsersDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ['OTP']
        # fields = '__all__'
