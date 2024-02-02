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
def create_contact(request):
    # try:
        requestData = remove_whitespace(request.data.copy())
        Phone_No = requestData['Phone_No']
        Profile_pic = requestData['Profile_pic'] if 'Profile_pic' in requestData else ''

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if Contacts.objects.filter(Phone_No = Phone_No).exists():
            return Response({"message":"Phone Number Already Exists", "status":201,"data":[]})

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        profile_pic_url = ""
        if Profile_pic:
            target ='./nexus/static/image/contacts'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+Profile_pic.name, Profile_pic)
            productImage_url = fss.url(file)
            profile_pic_url = productImage_url.replace('/nexus', '')
            requestData['Profile_pic'] = profile_pic_url
        print(profile_pic_url)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fetchJson = CreateContactsSerializer(data = requestData)
        if fetchJson.is_valid(raise_exception=True):
            fetchJson.save()
            contactObj = Contacts.objects.latest('id')
            # --------------------------------------------------
            for tag in requestData['Tags']:
                obj, temp = Tag.objects.get_or_create(Name = tag)
                contactObj.Tags.add(obj)

        return Response({"message":"successful", "status":200,"data":[]})
    # except Exception as e:
    #     return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def one_contact(request):
    try:
        contact_id = request.data['id']
        contact_obj = Contacts.objects.filter(pk = contact_id)
        result = ContactsSerializer(contact_obj, many=True)
        return Response({"message": "Success","status": 200,"data":result.data})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["GET"])
def all_contact(request):
    try:
        contact_obj = Contacts.objects.filter().order_by("-id")
        result = ContactsSerializer(contact_obj, many=True)
        return Response({"message": "Success","status": 200,"data":result.data})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def all_filter_page_contact(request):
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
        objs = Contacts.objects.filter(**json_data['field']).order_by(orderby)
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
        result = ContactsSerializer(objs, many=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        return Response({"message": "Success","status": 200,"data":result.data, "meta":{"count":count}})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def delete_contact(request):
    try:
        # Assuming the request contains an 'id' field indicating the contact to delete
        contact_id = request.data.get('id')
        # Fetch the contact object
        contact_obj = Contacts.objects.get(pk=contact_id)
        # Delete the contact
        contact_obj.delete()
        return Response({"message": "Contact deleted successfully", "status": 200, "data": []})
    except Contacts.DoesNotExist:
        return Response({"message": "Contact not found", "status": 201, "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data": []})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def update_contact(request):
    try:
        print("request.data", request.data)
        requestData = remove_whitespace(request.data.copy())
        fatchId     = requestData['id']
        Phone_No    = requestData['Phone_No'] if 'Phone_No' in requestData else ''
        Profile_pic = requestData['Profile_pic'] if 'Profile_pic' in requestData else ''

        if Contacts.objects.filter(Phone_No = Phone_No).exclude(pk = fatchId).exists():
            return Response({"message":"Phone Number Already Exists", "status":201,"data":[]})
        
        contactObj = Contacts.objects.get(pk = fatchId)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        profile_pic_url = ""
        if Profile_pic:
            target ='./nexus/static/image/contacts'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+Profile_pic.name, Profile_pic)
            productImage_url = fss.url(file)
            profile_pic_url = productImage_url.replace('/nexus', '')
            requestData['Profile_pic'] = profile_pic_url
        else:
            requestData['Profile_pic'] = contactObj.Profile_pic
        print(profile_pic_url)
        
        print("requestData2", requestData)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fetchJson = ContactsSerializer(instance=contactObj, data=requestData, partial=True)
        if fetchJson.is_valid(raise_exception=True):
            fetchJson.save()
            # tagsArr = requestData['Tags']
            for tag in requestData['Tags']:
                obj, temp = Tag.objects.get_or_create(Name = tag)
                contactObj.Tags.add(obj)

            # contactObj.Tags.add(*tagsArr)
        return Response({"message":"successful", "status":200,"data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def create_remarks(request):
    try:
        requestData = remove_whitespace(request.data.copy())
        fetchJson = RemarksSerializer(data = requestData)
        if fetchJson.is_valid(raise_exception=True):
            fetchJson.save()
            return Response({"message":"successful", "status":200,"data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def all_remarks(request):
    try:
        remarksObj = Remarks.objects.filter(Contact_Id = request.data['Contact_Id'])
        remarksjson = RemarksSerializer(remarksObj, many=True)
        return Response({"message":"successful", "status":200,"data":remarksjson.data})
    except Exception as e:
        return Response({"message":str(e), "status":201, "data":[]})