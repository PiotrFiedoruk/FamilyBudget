# filters.py
import datetime
from rest_framework import filters


class BudgetDateRangeFilter(filters.BaseFilterBackend):
    """
    Filters Budgets based on date of related Budget Operations. Returns only Budgets with BudgetOperations date in range
    """
    def filter_queryset(self, request, queryset, view):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            return queryset.filter(operations__date__range=[start_date, end_date]).distinct()
        return queryset


class BudgetOperationDateRangeFilter(filters.BaseFilterBackend):
    """
    Filters Budget Operations based on date. Returns only BudgetOperations with date in range
    """
    def filter_queryset(self, request, queryset, view):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            return queryset.filter(date__range=[start_date, end_date]).distinct()
        return queryset


class BudgetSharedFilter(filters.BaseFilterBackend):
    """
    Depending on type returns budgets that are owned, or shared by other users. Defaults to both
    """
    def filter_queryset(self, request, queryset, view):
        user = request.user
        type = request.query_params.get('type')
        if type == 'shared':
            return queryset.filter(shared_with=user)
        if type == 'owned':
            return queryset.filter(owner=user)
        return queryset


class BudgetOperationBudgetIdFilter(filters.BaseFilterBackend):
    """
    Return BudgetOperations related to Budget matching budget_id param
    """
    def filter_queryset(self, request, queryset, view):
        budget_id = request.query_params.get('budget_id')
        if budget_id:
            return queryset.filter(budget_id=budget_id)
        return queryset
