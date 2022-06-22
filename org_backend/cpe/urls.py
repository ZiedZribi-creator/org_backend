from django.urls import path
from .views import (cpe_list,cpe_detail,create_cpe,delete_cpe,update_cpe,get_cpe,
                    reboot_cpe)

urlpatterns = [
    path('cpe_list', cpe_list),
    path('create_cpe', create_cpe),
    path('cpe/<int:id>', cpe_detail),
    path('delete_cpe', delete_cpe),
    path('cpe/<int:id>/update', update_cpe),
    path('cpe/<int:id>/status', get_cpe),
    path('cpe/<int:id>/reboot', reboot_cpe),
]