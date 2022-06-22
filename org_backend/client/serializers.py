from asyncore import write
from dataclasses import field
from rest_framework import serializers
from .models import Client
from cpe.serializers import CpeSerializer 
import os 
import binascii



class ClientSerializer(serializers.ModelSerializer):
    cpe_count = serializers.SerializerMethodField()
    cpe_list  = serializers.SerializerMethodField()
    client_id = serializers.IntegerField(write_only=True,required=False)
    class Meta : 
        model = Client
        fields = ('id','email','username','tel','city','address','client_id','cpe_list','cpe_count')
        
    def get_cpe_count(self,client_obj):
        return client_obj.cpe_set.all().count()

    def get_cpe_list(self,client_obj):
        qs =  client_obj.cpe_set.all()
        ser = CpeSerializer(qs,many=True)
        return ser.data 

    def validate(self,data):
        print("validating")
        client_id = data.get('client_id')
        print(f"client id : {client_id}")
        if client_id : # for update
            print(f"client id : {client_id}")
            client_obj = Client.objects.get(id=client_id)
            print(f"client_obj.email  : {client_obj.email}")
            print(f"data['email']   : {data['email']}")
            if client_obj.email != data['email'] : 
                qs = Client.objects.filter(email=data['email'] )
                if qs :
                    print("email already exist")
                    raise serializers.ValidationError('email already exist')
        else : # for create
            qs = Client.objects.filter(email=data['email'] )
            if qs :
                print("email already exist")
                raise serializers.ValidationError('email already exist')

        return data



