from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Budget, BudgetOperation

User = get_user_model()


class BudgetOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetOperation
        fields = ['budget', 'category', 'amount', 'date']


class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = ['id', 'name', 'owner', 'shared_with']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class BudgetDetailedSerializer(serializers.ModelSerializer):
    operations = BudgetOperationSerializer(many=True)
    shared_with = UserSerializer(many=True)

    class Meta:
        model = Budget
        fields = ['id', 'name', 'owner', 'shared_with', 'operations']



