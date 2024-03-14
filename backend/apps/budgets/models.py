from django.db import models
from django.conf import settings


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

    def __str__(self):
        return self.name
