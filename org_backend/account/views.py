from pickle import TRUE
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from .models import Technicien, User
from .serializers import AdminSerializer, TechnicienSerializer,UpdateTechnicienSerializer
from .permissions import IsAdminOrDeny
from cpe.models import Cpe


class TechnicienViewSet(viewsets.ModelViewSet):
    serializer_class = TechnicienSerializer
    queryset = Technicien.objects.all()
    permission_classes = (IsAdminOrDeny,)


    def list(self, request, *args, **kwargs):
        qs = Technicien.objects.all()
        email = request.GET.get('email')
        working_city = request.GET.get('working_city')
        if email : 
            qs = qs.filter(user__email=email)
        if working_city :
            qs = qs.filter(working_city=working_city)
        serializer = TechnicienSerializer(qs, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        tech_ids = request.data.get('tech_ids')
        for tech_id in tech_ids : 
            tech_obj = Technicien.objects.get(id=tech_id)
            tech_obj.user.delete()
            #tech_obj.delete()
        return Response(data={"msg":"tech ids were deleted"})

    @action(methods=['DELETE'],detail=False)
    def delete_techs(self,request):
        tech_ids = request.data.get('tech_ids')
        for tech_id in tech_ids : 
            tech_obj = Technicien.objects.get(id=tech_id)
            tech_obj.user.delete()
            #tech_obj.delete()
        return Response(data={"msg":"tech ids were deleted"})

    @action(methods=['PUT'],detail=True)
    def add_cpe(self,request,pk):
        tech_obj = self.get_object()
        cpe_ids = request.data.get('cpe_ids')
        for cpe_id in cpe_ids : 
            cpe_obj_qs = Cpe.objects.filter(id=cpe_id)
            cpe_obj_qs.update(technicien=tech_obj)
        return Response({"msg":"the cpe(s) were added to the tech successfully"},status=status.HTTP_200_OK) 

    @action(methods=['PUT'],detail=False)
    def remove_cpe(self,request):
        cpe_ids = request.data.get('cpe_ids')
        for cpe_id in cpe_ids : 
            cpe_obj_qs = Cpe.objects.filter(id=cpe_id)
            cpe_obj_qs.update(technicien=None)
        return Response({"msg":"the cpe(s) were removed from the tech successfully"},status=status.HTTP_200_OK) 

    @action(methods=['PUT'],detail=True)
    def update_tech(self,request,pk):
        qs = Technicien.objects.filter(id=pk)
        ser = UpdateTechnicienSerializer(data=request.data)
        print('viewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
        print(request.data)
        if ser.is_valid(): 
            print('is valid :::::::::::::::::::::::::::::::::::::::')
            print(request.data)
            user_obj = qs.first().user 
            user_obj.email = request.data['email']
            user_obj.username = request.data['username']
            user_obj.save()
            del request.data['email']
            del request.data['username']
            qs.update(**request.data)
            return Response({"msg":"the tech were updated successfully"},status=status.HTTP_200_OK) 
        return Response({"error_msg": "invalid fields"},status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def tech_detail(request,id):
    if request.user.is_authenticated :
        qs = Technicien.objects.filter(id=id)
        if qs : 
            tech_obj = qs.first()
            if request.user.is_admin or request.user == tech_obj.user: 
                tech_ser = TechnicienSerializer(tech_obj)
                return Response(tech_ser.data,status=status.HTTP_200_OK) 
            return Response({'error_msg':'you are not allowed to access this technicien'},status=status.HTTP_403_FORBIDDEN)
        return Response({"error_msg": "this cpe not found"},status=status.HTTP_404_NOT_FOUND)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def admin_detail(request,id):
    if request.user.is_authenticated and request.user.is_admin :
        qs = User.objects.filter(id=id)
        if qs : 
            admin_obj = qs.first()
            ser = AdminSerializer(admin_obj)
            return Response(ser.data,status=status.HTTP_200_OK) 
        return Response({"error_msg": "this admin not found"},status=status.HTTP_404_NOT_FOUND)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def admin_update(request,id):
    if request.user.is_authenticated and request.user.is_admin :
        qs = User.objects.filter(id=id)
        if qs : 
            admin_obj = qs.first()
            data = request.data
            print(data)
            ser = AdminSerializer(data=data)
            if ser.is_valid(): 
                print("valid")
                old_password = data['old_password']
                if admin_obj.check_password(old_password) : # you have the perm to update the admin 
                    new_password = data.get('new_password')
                    if new_password and old_password != new_password : 
                        admin_obj.set_password(new_password)
                        admin_obj.save()
                        print('update pass')
                    email = data.get('email')
                    if email : 
                        admin_obj.email =email
                        admin_obj.save()
                        print('update email')
                    username = data.get('username')
                    if username : 
                        admin_obj.username =username
                        admin_obj.save()
                        print('update username')
                else : 
                    return Response({"error_msg": "Invalid old password"},status=status.HTTP_401_UNAUTHORIZED)
                return Response({"msg": "the admin were update"},status=status.HTTP_200_OK)
            return Response({"error_msg": "invalid fields"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"error_msg": "this admin not found"},status=status.HTTP_404_NOT_FOUND)
    return Response({"error_msg": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)
