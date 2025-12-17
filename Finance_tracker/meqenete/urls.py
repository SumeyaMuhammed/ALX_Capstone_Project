from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterAPIView, LoginAPIView, CategoryViewSet, ExpenseViewSet, IncomeViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'income', IncomeViewSet, basename='income')



urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
]

urlpatterns += router.urls