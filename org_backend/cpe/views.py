from http import client
from django.shortcuts import render
from account.models import Technicien

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cpe
from client.models import Client
from .serializers import CpeSerializer, UpdateCpeSerializer


@api_view(['GET'])
def cpe_list(request):
    if request.user.is_authenticated : 
        qs = Cpe.objects.all()
        if request.user.is_admin:
            tech_id = request.GET.get('tech_id')
            if tech_id:
                tech_obj= Technicien.objects.get(id=tech_id)
                print(tech_id)
                qs=qs.exclude(technicien__id=tech_obj.id)#client=None,
                qs = qs.filter(client__city=tech_obj.working_city)
                print(qs)
                ser = CpeSerializer(qs,many=True)
                return Response(ser.data,status=status.HTTP_200_OK)
            client_id = request.GET.get('client_id')
            if client_id:
                qs=qs.filter(client=None)
                ser = CpeSerializer(qs,many=True)
                return Response(ser.data,status=status.HTTP_200_OK)
            client
        order_by = request.GET.get('order_by')
        status_ = request.GET.get('status')
        city = request.GET.get('city')
        if city : 
            qs = qs.filter(client__city=city)
        if status_ : 
            status_ = True if status_ == 'true' else False 
            print("status ::::::::::::::::::::")
            print(status_)
            qs = qs.filter(status__in=[status_])
            print(qs)
        if order_by : 
            qs = qs.order_by(f"-{order_by}")
        if hasattr(request.user, 'technicien')  : 
            tech_obj = request.user.technicien
            qs = qs.filter(technicien=tech_obj)
        ser = CpeSerializer(qs,many=True)
        return Response(ser.data,status=status.HTTP_200_OK)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def cpe_detail(request,id):
    if request.user.is_authenticated : 
        qs = Cpe.objects.filter(id=id)
        if qs : 
            cpe_obj = qs.first()
            if hasattr(request.user, 'technicien')  : 
                tech_obj = request.user.technicien
                if cpe_obj.technicien != tech_obj : 
                    return Response({'error_msg':'you are not allowed to access this cpe'},status=status.HTTP_403_FORBIDDEN)
            ser = CpeSerializer(cpe_obj)
            return Response(ser.data,status=status.HTTP_200_OK)
        return Response({"error_msg": "this cpe not found"},status=status.HTTP_404_NOT_FOUND)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)

import random
import string

def get_random_token(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    token = ''.join(random.choice(letters) for i in range(length))
    qs = Cpe.objects.filter(token=token)
    if qs : 
        get_random_token(length)
    return token 

@api_view(['POST'])
def create_cpe(request):
    if request.user.is_authenticated and request.user.is_admin : 
        token = get_random_token(50)
        Cpe.objects.create(token=token)
        return Response({'res':'the cpe was created'},status=status.HTTP_200_OK)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_cpe(request,id):
    token = request.data.get('token')
    del request.data['token']
    if token : 
        qs = Cpe.objects.filter(id=id)
        if qs : 
            print("cpe exist")
            real_owned_cpe_obj = Cpe.objects.get(token=token)
            claim_owned_cpe_obj = qs.first()
            if real_owned_cpe_obj == claim_owned_cpe_obj : 
                print("owned")
                print(request.data)
                cpe_obj = qs.first()
                return Response({"status":cpe_obj.status},status=status.HTTP_200_OK)
        return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED) 

@api_view(['PUT'])
def update_cpe(request,id):
    token = request.data.get('token')
    del request.data['token']
    if token : 
        qs = Cpe.objects.filter(id=id)
        if qs : 
            print("cpe exist")
            real_owned_cpe_obj = Cpe.objects.get(token=token)
            claim_owned_cpe_obj = qs.first()
            if real_owned_cpe_obj == claim_owned_cpe_obj : 
                print("owned")
                print(request.data)
                ser = UpdateCpeSerializer(data=request.data)
                if ser.is_valid(): 
                    qs.update(**request.data)
                    cpe_obj = qs.first()
                    return Response({'msg':'cpe has been updated'},status=status.HTTP_200_OK)
                else : 
                    print("invalid format")
        return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED) 


@api_view(['DELETE'])
def delete_cpe(request):
    if request.user.is_authenticated and request.user.is_admin  : 
        cpe_ids = request.data.get("cpe_ids")
        for cpe_id in cpe_ids : 
            cpe_obj = Cpe.objects.get(id=cpe_id)
            cpe_obj.delete()
        return Response({"msg":"he cpe(s) were successfully deleted"},status=status.HTTP_200_OK)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def reboot_cpe(request,id):
    if request.user.is_authenticated : 
        qs = Cpe.objects.filter(id=id)
        if qs :
            if hasattr(request.user, 'technicien')  : 
                tech_obj = request.user.technicien
                cpe_obj = qs.first()
                if cpe_obj.technicien != tech_obj : 
                    return Response({'error_msg':'you are not allowed to access this cpe'},status=status.HTTP_403_FORBIDDEN)
            qs.update(status = False,    
                    upload_debit = 0.0,
                    download_debit = 0.0,
                    temperature = 0.0,
                    cpu_usage = 0.0,
                    ram_usage = 0.0)
            return Response({"msg":"the cpe was successfully rebooted"},status=status.HTTP_200_OK)
        return Response({"error_msg": "no cpe found"},status=status.HTTP_404_NOT_FOUND)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)
