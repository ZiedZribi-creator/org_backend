from django.urls import path
from .views import (client_detail, client_list, create_client, delete_client, update_client,
                    remove_cpe_from_client,add_cpe_to_client)

urlpatterns = [
    path('client_list', client_list),
    path('client/<int:id>', client_detail),
    path('create_client', create_client),
    path('client/<int:id>/delete', delete_client),
    path('client/<int:id>/update', update_client),
    path('client/<int:id>/update', update_client),
    path('client/<int:id>/add_cpe', add_cpe_to_client),
    path('client/remove_cpe', remove_cpe_from_client),



]