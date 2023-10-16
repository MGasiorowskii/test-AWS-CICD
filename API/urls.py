from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PhotosViewSet


router = SimpleRouter()
router.register(r'photos', PhotosViewSet, basename='photos')

urlpatterns = [
    path('', include(router.urls)),
]
