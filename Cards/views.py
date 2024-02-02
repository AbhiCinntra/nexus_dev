from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render, redirect  
import requests, json
from django.contrib import messages
from rest_framework.decorators import api_view    
from rest_framework.response import Response

from django.db.models import Q 

from .models import *
from .serializers import *
from global_fun import remove_whitespace, PAGE

import os
from django.core.files.storage import FileSystemStorage
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create your views here. 
@api_view(['POST'])
def create_card(request):
    try:
        Phone_No = request.data['Phone_No']
        Profile_pic = request.data['Profile_pic'] if 'Profile_pic' in request.data else ''

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if Cards.objects.filter(Phone_No = Phone_No).exists():
            return Response({"message":"Phone Number Already Exists", "status":201,"data":[]})

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        profile_pic_url = ""
        if Profile_pic:
            target ='./nexus/static/image/cards'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+Profile_pic.name, Profile_pic)
            productImage_url = fss.url(file)
            profile_pic_url = productImage_url.replace('/nexus', '')
            request.data['Profile_pic'] = profile_pic_url

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        print(profile_pic_url)
        requestData = remove_whitespace(request.data)
        fetchJson = CardsSerializer(data = requestData)
        if fetchJson.is_valid(raise_exception=True):
            fetchJson.save()

        return Response({"message":"successful", "status":200,"data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def one_card(request):
    try:
        card_id = request.data['id']
        card_obj = Cards.objects.filter(pk = card_id)
        result = CardsSerializer(card_obj, many=True)
        return Response({"message": "Success","status": 200,"data":result.data})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["GET"])
def all_card(request):
    try:
        card_obj = Cards.objects.filter().order_by("-id")
        result = CardsSerializer(card_obj, many=True)
        return Response({"message": "Success","status": 200,"data":result.data})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def all_filter_page_card(request):
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
        objs = Cards.objects.filter(**json_data['field']).order_by(orderby)
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
        result = CardsSerializer(objs, many=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        return Response({"message": "Success","status": 200,"data":result.data, "meta":{"count":count}})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def delete_card(request):
    try:
        # Assuming the request contains an 'id' field indicating the card to delete
        card_id = request.data.get('id')
        # Fetch the card object
        card_obj = Cards.objects.get(pk=card_id)
        # Delete the card
        card_obj.delete()
        return Response({"message": "Cards deleted successfully", "status": 200, "data": []})
    except Cards.DoesNotExist:
        return Response({"message": "Cards not found", "status": 201, "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data": []})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def update_card(request):
    try:
        print("request.data", request.data)
        requestData = remove_whitespace(request.data.copy())
        fatchId     = requestData['id']
        Phone_No    = requestData['Phone_No'] if 'Phone_No' in requestData else ''
        Profile_pic = requestData['Profile_pic'] if 'Profile_pic' in requestData else ''

        if Cards.objects.filter(Phone_No = Phone_No).exclude(pk = fatchId).exists():
            return Response({"message":"Phone Number Already Exists", "status":201,"data":[]})
        
        RoleObj = Cards.objects.get(pk = fatchId)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        profile_pic_url = ""
        if Profile_pic:
            target ='./nexus/static/image/cards'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+Profile_pic.name, Profile_pic)
            productImage_url = fss.url(file)
            profile_pic_url = productImage_url.replace('/nexus', '')
            requestData['Profile_pic'] = profile_pic_url
        else:
            requestData['Profile_pic'] = RoleObj.Profile_pic

        # print("profile_pic_url", profile_pic_url, "Profile_pic", Profile_pic)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fetchJson = CardsSerializer(instance=RoleObj, data=requestData, partial=True)
        if fetchJson.is_valid():
            fetchJson.save()       
        else :
            return Response({"message":str(fetchJson.error_messages['invalid']), "status":201, "data":[]})
        return Response({"message":"successful", "status":200,"data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>