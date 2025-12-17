from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterAPIView, LoginAPIView, CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
]

urlpatterns += router.urls