from rest_framework import generics, permissions
from .serializers import RegisterSerializer, LoginSerializer
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView



class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer

