from django.urls import path
from .views import TechnicienViewSet,tech_detail,admin_detail,admin_update
from rest_framework import routers
from django.conf.urls import include


router = routers.DefaultRouter()
router.register('tech', TechnicienViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('admin/<int:id>/',admin_detail),
    path('tek/<int:id>/',tech_detail),
    path('admin/<int:id>/update/',admin_update),
]