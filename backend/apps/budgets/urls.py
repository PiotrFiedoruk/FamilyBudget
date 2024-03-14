from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BudgetViewSet, BudgetOperationViewSet, UserViewSet

router = DefaultRouter()
router.register(r'budgets', BudgetViewSet, basename='budgets')
router.register(r'operations', BudgetOperationViewSet, basename='operations')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('api/', include(router.urls)),
]