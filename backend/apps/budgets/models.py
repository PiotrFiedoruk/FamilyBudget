from decimal import Decimal

from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.
class Budget(models.Model):
    """
    Budget model wraps BudgetOperation objects and ties them to user.
    """
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_with', blank=True)

    class Meta:
        unique_together = ['name', 'owner']
        ordering = ('name',)

    def __str__(self):
        return self.name


class BudgetOperation(models.Model):
    """
    Model holding budget operations. Incomes have positive amount, expenses negative.
    """

    category = models.CharField(max_length=256)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='operations')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    date = models.DateField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.category
