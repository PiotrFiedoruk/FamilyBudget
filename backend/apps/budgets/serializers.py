from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Budget, BudgetOperation

User = get_user_model()


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'name', 'owner', 'shared_with']


class BudgetOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetOperation
        fields = ['budget', 'category', 'amount', 'date']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
