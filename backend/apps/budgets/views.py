from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .models import Budget, BudgetOperation
from .serializers import BudgetSerializer, BudgetDetailedSerializer, BudgetOperationSerializer, UserSerializer
from .filters import (BudgetDateRangeFilter, BudgetOperationDateRangeFilter, BudgetSharedFilter,
                      BudgetOperationBudgetIdFilter)
from .permissions import IsOwnerOrShared


class BudgetViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        # adds details for any foreign relations fields if ?detail=true
        if self.request.query_params.get('detailed') == 'true':
            return BudgetDetailedSerializer
        return BudgetSerializer

    filter_backends = [SearchFilter, BudgetDateRangeFilter, BudgetSharedFilter]
    permission_classes = [IsOwnerOrShared]
    search_fields = ['name']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Budget.objects.all()
        return Budget.objects.filter(Q(owner=self.request.user) | Q(shared_with=self.request.user)).distinct()


class BudgetOperationViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetOperationSerializer
    filter_backends = [SearchFilter, BudgetOperationBudgetIdFilter, BudgetOperationDateRangeFilter]
    search_fields = ['category']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return BudgetOperation.objects.all()
        return BudgetOperation.objects.filter(Q(budget__owner=self.request.user) | Q(budget__shared_with=self.request.user)).distinct()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    User = get_user_model()
    queryset = User.objects.all()
