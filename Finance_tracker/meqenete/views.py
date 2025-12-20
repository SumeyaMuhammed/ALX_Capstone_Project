from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from decimal import Decimal
from .models import User, Category, Expense, Income
from .serializers import RegisterSerializer, LoginSerializer, CategorySerializer, ExpenseSerializer, IncomeSerializer
from .pagination import StandardResultsPagination




class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ---------- Filters ----------

class ExpenseFilter(filters.FilterSet):
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    month = filters.NumberFilter(field_name='date', lookup_expr='month')
    year = filters.NumberFilter(field_name='date', lookup_expr='year')

    class Meta:
        model = Expense
        fields = ['category_name', 'month', 'year']

class IncomeFilter(filters.FilterSet):
    month = filters.NumberFilter(field_name='date', lookup_expr='month')
    year = filters.NumberFilter(field_name='date', lookup_expr='year')

    # Optional: allow source filtering by exact string
    source = filters.CharFilter(field_name='source', lookup_expr='iexact')

    class Meta:
        model = Income
        fields = ['source', 'month', 'year']


class ExpenseViewSet(ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        expense = self.get_object()
        if expense.status == 'APPROVED':
            return Response({'detail': 'Expense already approved.'}, status=status.HTTP_400_BAD_REQUEST)
        expense.status = 'APPROVED'
        expense.save()
        return Response({'detail': 'Expense approved.'})

    @action(detail=True, methods=['post'])
    def revert(self, request, pk=None):
        expense = self.get_object()
        if expense.status == 'PENDING':
            return Response({'detail': 'Expense already pending.'}, status=status.HTTP_400_BAD_REQUEST)
        expense.status = 'PENDING'
        expense.save()
        return Response({'detail': 'Expense reverted to pending.'})

class IncomeViewSet(ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['source']

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MonthlySummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            return Response(
                {"error": "month and year are required"},
                status=400
            )

        incomes = Income.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year
        ).aggregate(total_income=Sum('amount'))

        expenses = Expense.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year
        ).aggregate(total_expense=Sum('amount'))

        total_income = incomes['total_income'] or Decimal('0.00')
        total_expense = expenses['total_expense'] or Decimal('0.00')

        return Response({
            "month": int(month),
            "year": int(year),
            "total_income": f"{total_income:.2f}",
            "total_expense": f"{total_expense:.2f}",
            "balance": f"{total_income - total_expense:.2f}"
        })