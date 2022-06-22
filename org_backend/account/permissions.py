
from rest_framework import permissions

class IsAdminOrDeny(permissions.BasePermission):

    def has_permission(self, request, view):

        if not(request.user.is_authenticated) : 
            return False 
        return request.user.is_admin 

#request.user.technicien == tech_obj