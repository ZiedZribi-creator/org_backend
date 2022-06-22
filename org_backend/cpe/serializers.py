from dataclasses import field
from rest_framework import serializers
from .models import Cpe
import os 
import binascii

class CpeSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    token = serializers.CharField(read_only=True)
    tech_email = serializers.SerializerMethodField()

    class Meta : 
        model = Cpe
        fields = ('id','client','token'
        ,'status','upload_debit','download_debit',
        'temperature','cpu_usage','ram_usage','tech_email')

    def get_tech_email(self,cpe_obj):
        if cpe_obj.technicien : 
            return cpe_obj.technicien.user.email 
        return 'none' 

    def get_client(self,cpe_obj):
        client_obj = cpe_obj.client
        return self.client_obj_to_json(client_obj)

    def create(self,validated_data): 
        cpe_obj = Cpe.objects.create(**validated_data)
        cpe_obj.token = binascii.hexlify(os.urandom(20)).decode()
        cpe_obj.save()
        return cpe_obj
    
    def client_obj_to_json(self,client_obj): 
        data = {}
        if client_obj : 
            data['email'] = client_obj.email
            data['username'] = client_obj.username
            data['tel'] = client_obj.tel
            data['city'] = client_obj.city
            data['address'] = client_obj.address
        return data

class UpdateCpeSerializer(serializers.ModelSerializer):
     class Meta : 
        model = Cpe
        fields = ('status','upload_debit','download_debit','temperature','cpu_usage','ram_usage',)
