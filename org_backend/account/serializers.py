from asyncore import write
from dataclasses import field

from pkg_resources import require
from rest_framework import serializers
from .models import Technicien,User
from cpe.serializers import CpeSerializer

class AdminSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True,allow_blank=True)
    confirm_new_password = serializers.CharField(write_only=True,allow_blank=True)
    old_password = serializers.CharField(write_only=True)
    user_id = serializers.CharField(write_only=True)
    class Meta : 
        fields = ('id','email','username','new_password','confirm_new_password','old_password','user_id')
    
    def validate(self,data):
        print("validate")
        user_id = data['user_id']
        user_obj = User.objects.get(id=user_id)
        if user_obj.email != data['email'] : 
            qs = User.objects.filter(email=data['email'] )
            if qs :
                print("email already exist")
                raise serializers.ValidationError('email already exist')
        return data



class TechnicienSerializer(serializers.ModelSerializer):
    cpe_count = serializers.SerializerMethodField()
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    password = serializers.CharField(style={'input_type':'password'},write_only=True,required=True)
    cpe_list  = serializers.SerializerMethodField()
    class Meta : 
        model = Technicien
        fields = ('id','email','username','tel','city','working_city','password','cpe_list','cpe_count')



    def get_cpe_count(self,tech_obj):
        return tech_obj.cpe_set.all().count()

    def get_cpe_list(self,tech_obj):
        qs =  tech_obj.cpe_set.all()
        ser = CpeSerializer(qs,many=True)
        return ser.data 
    
    def validate(self,data):
        email = data.get('user').get('email') 
        print(email)
        qs = User.objects.filter(email=email)
        print(qs)
        if qs :
            print("email already exist")
            raise serializers.ValidationError('email already exist')
        return data

    def create(self,validated_data):
        print(validated_data)
        user_data = validated_data['user']
        del validated_data['user']
        user_obj = User.objects.create(**user_data)
        user_obj.set_password(validated_data['password'])
        user_obj.save()
        del validated_data['password']
        tech_obj = Technicien.objects.create(**validated_data)
        tech_obj.user = user_obj 
        tech_obj.save()
        return tech_obj

    def update(self, tech_obj, validated_data):
        print(validated_data)
        return tech_obj

class UpdateTechnicienSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    #tech_id = serializers.IntegerField(write_only=True)

    class Meta :
        model = Technicien
        fields = ('id','email','username','tel','city','working_city','tech_id')

    def validate(self,data):
        tech_id = data['tech_id']
        tech_obj = Technicien.objects.get(id=tech_id)
        if tech_obj.user.email != data['user']['email'] : 
            qs = User.objects.filter(email=data['user']['email'] )
            if qs :
                print("email already exist")
                raise serializers.ValidationError('email already exist')
        return data



