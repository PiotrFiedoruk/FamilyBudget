from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Budget, BudgetOperation


# Register your models here.
@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')


@admin.register(BudgetOperation)
class BudgetOperationAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'budget')
