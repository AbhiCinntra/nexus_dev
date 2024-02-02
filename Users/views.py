from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render, redirect  
import requests, json
from django.contrib import messages
from rest_framework.decorators import api_view    
from rest_framework.response import Response

from django.db.models import Q

from Cards.serializers import CardsSerializer 

from .models import *
from .serializers import *
from global_fun import remove_whitespace, PAGE

import os
from django.core.files.storage import FileSystemStorage
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import random
def generate_otp():
    return str(random.randint(1000, 9999))
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create your views here. 
@api_view(['POST'])
def create_user(request):
    try:
        Phone_No = request.data['Phone_No']
        Profile_pic = request.data['Profile_pic'] if 'Profile_pic' in request.data else ''

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if Users.objects.filter(Phone_No = Phone_No).exists():
            return Response({"message":"Phone Number Already Exists", "status":201,"data":[]})

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        profile_pic_url = ""
        if Profile_pic:
            target ='./nexus/static/image/users'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+Profile_pic.name, Profile_pic)
            productImage_url = fss.url(file)
            profile_pic_url = productImage_url.replace('/nexus', '')
            request.data['Profile_pic'] = profile_pic_url

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        print(profile_pic_url)
        requestData = remove_whitespace(request.data)
        fetchJson = UsersSerializer(data = requestData)
        if fetchJson.is_valid(raise_exception=True):
            fetchJson.save()
            # userObj = Users.objects.latest('id')
            # requestData['User_Id'] = userObj.id
            # fetchCardJson = CardsSerializer(data = requestData)
            # fetchCardJson.save()
        return Response({"message":"successful", "status":200,"data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def login_user(request):
    try:
        Country_Code = request.data['Country_Code']
        Phone_No = request.data['Phone_No']
        user_obj = Users.objects.filter(Phone_No = Phone_No)
        # create otp for user
        otp = generate_otp()

        if user_obj.exists():
            user_obj.update(OTP = otp)
        else:
            Users(Country_Code = Country_Code, Phone_No = Phone_No, OTP = otp ).save()
            
        return Response({"message": "Success","status": 200,"data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# {"Phone_No": "1234567890", "OTP": "5563"}
@api_view(["POST"])
def verify_user(request):
    # try:
        Phone_No    = request.data['Phone_No']
        requestOtp  = request.data['OTP']
        user_obj    = Users.objects.filter(Phone_No = Phone_No)
        if user_obj.exists():
            user_obj = user_obj.first()
            print(user_obj.OTP, requestOtp)
            # if str(user_obj.OTP) == str(requestOtp):
            if True:
                result = UsersDetailsSerializer(user_obj, many=False)
                return Response({"message": "Success","status": 200,"data":[result.data]})
            else:
                return Response({"message": "Invalid OTP","status": 201,"data":[]})
        else:
            return Response({"message": "Invalid User ","status": 201,"data":[]})
            
    # except Exception as e:
    #     return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def one_user(request):
    try:
        user_id = request.data['id']
        user_obj = Users.objects.filter(pk = user_id)
        result = UsersSerializer(user_obj, many=True)
        return Response({"message": "Success","status": 200,"data":result.data})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["GET"])
def all_user(request):
    try:
        user_obj = Users.objects.filter().order_by("-id")
        result = UsersSerializer(user_obj, many=True)
        return Response({"message": "Success","status": 200,"data":result.data})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def all_filter_page_user(request):
    try:
        json_data       = request.data
        SearchText      = json_data['SearchText']
        page            = PAGE(json_data)
        order_by_field  = json_data['order_by_field']
        order_by_value  = json_data['order_by_value']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = "-id"
        if str(order_by_field).strip() != "":
            orderby = f"{order_by_field}"
            if str(order_by_value).lower() == 'desc':
                orderby = f"-{order_by_field}"
            # endif
        # endif
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        objs = Users.objects.filter(**json_data['field']).order_by(orderby)
        if str(SearchText) != "":
            objs = objs.filter(
                Q(pk__icontains=SearchText) |
                Q(Phone_No__icontains=SearchText) |
                Q(User_Name__icontains=SearchText) |
                Q(Email_Id__icontains=SearchText) |
                Q(Company_Name__icontains=SearchText) |
                Q(Designation_Name__icontains=SearchText) |
                Q(Address__icontains=SearchText)
            ).order_by(orderby)
        # endif
        count = objs.count()
        objs = objs[page['startWith']:page['endWith']]
        result = UsersSerializer(objs, many=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        return Response({"message": "Success","status": 200,"data":result.data, "meta":{"count":count}})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def update_user(request):
    try:
        requestData = remove_whitespace(request.data)
        fatchId     = requestData['id']
        Phone_No    = requestData['Phone_No'] if 'Phone_No' in requestData else ''
        Profile_pic = requestData['Profile_pic'] if 'Profile_pic' in requestData else ''

        if Users.objects.filter(Phone_No = Phone_No).exclude(pk = fatchId).exists():
            return Response({"message":"Phone Number Already Exists", "status":201,"data":[]})
        
        RoleObj = Users.objects.get(pk = fatchId)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        profile_pic_url = ""
        if Profile_pic:
            target ='./nexus/static/image/users'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+Profile_pic.name, Profile_pic)
            productImage_url = fss.url(file)
            profile_pic_url = productImage_url.replace('/nexus', '')
            requestData['Profile_pic'] = profile_pic_url
        else:
            requestData['Profile_pic'] = RoleObj.Profile_pic
        print(profile_pic_url)

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fetchJson = UsersSerializer(RoleObj, data = requestData)
        if fetchJson.is_valid():
            fetchJson.save()
        # end if
        return Response({"message":"successful", "status":200,"data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>