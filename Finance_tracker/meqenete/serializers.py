from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Category, Expense, Income


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(TokenObtainPairSerializer):
    username_field = 'email'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']


class ExpenseSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if self.instance and self.instance.status == 'APPROVED':
            raise serializers.ValidationError("Cannot edit an approved expense.")
        return data

    def validate_category(self, value):
        request = self.context['request']
        if value.user != request.user:
            raise serializers.ValidationError(
                "You can only use your own categories."
            )
        return value
    
    class Meta:
        model = Expense
        fields = ['id', 'category', 'amount', 'description', 'date', 'created_at', 'status']


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'source', 'amount', 'date', 'created_at'
        ]
