from xmlrpc import client
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Client
from client.models import Client
from cpe.models import Cpe
from .serializers import ClientSerializer

# Create your views here.
@api_view(['GET'])
def client_list(request):
    if request.user.is_authenticated and request.user.is_admin : 
        qs = Client.objects.all()
        email = request.GET.get('email')
        city = request.GET.get('city')
        if email : 
            qs = qs.filter(email=email)
        if city : 
            qs = qs.filter(city=city)
        print(qs)
        ser = ClientSerializer(qs,many=True)
        return Response(ser.data,status=status.HTTP_200_OK)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def client_detail(request,id):
    if request.user.is_authenticated and request.user.is_admin : 
        qs = Client.objects.filter(id=id)
        if qs : 
            client_obj = qs.first()
            ser = ClientSerializer(client_obj)
            return Response(ser.data,status=status.HTTP_200_OK)
        return Response({"error_msg": "this client not found"},status=status.HTTP_404_NOT_FOUND)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def create_client(request):
    if request.user.is_authenticated and request.user.is_admin: 
        ser = ClientSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data,status=status.HTTP_200_OK)
        return Response({"error_msg": "invalid fields"},status=status.HTTP_400_BAD_REQUEST)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
def delete_client(request,id):
    if request.user.is_authenticated and request.user.is_admin: 
        qs = Client.objects.filter(id=id)
        if qs : 
            client_obj = qs.first()
            client_obj.delete()
            return Response({"msg":"the client was successfully deleted"},status=status.HTTP_200_OK)
        return Response({"error_msg": "no client found"},status=status.HTTP_404_NOT_FOUND)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def update_client(request,id):
    if request.user.is_authenticated and request.user.is_admin: 
        print(request.data)
        qs = Client.objects.filter(id=id)
        if qs : 
            ser = ClientSerializer(data=request.data)
            if ser.is_valid() : 
                qs.update(**request.data) # {"key":"value"} key=value
                return Response({"msg":"client was updated"},status=status.HTTP_200_OK)
            return Response({"error_msg": "invalid fields"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"error_msg": "no client found"},status=status.HTTP_404_NOT_FOUND)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def add_cpe_to_client(request,id):
    if request.user.is_authenticated and request.user.is_admin: 
        qs = Client.objects.filter(id=id)
        if qs : 
            client_obj = qs.first()
            cpe_ids = request.data.get('cpe_ids')
            for cpe_id in cpe_ids : 
                qs_cpe_obj = Cpe.objects.filter(id=cpe_id)
                qs_cpe_obj.update(client=client_obj)
            return Response({"msg":"cpe's were added !!"},status=status.HTTP_200_OK)
        return Response({"error_msg": "no client found"},status=status.HTTP_404_NOT_FOUND)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def remove_cpe_from_client(request):
    if request.user.is_authenticated and request.user.is_admin: 
        cpe_ids = request.data.get('cpe_ids')
        for cpe_id in cpe_ids : 
            qs_cpe_obj = Cpe.objects.filter(id=cpe_id)
            qs_cpe_obj.update(client=None)
        return Response({"msg":"cpe's were removed !!"},status=status.HTTP_200_OK)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)
