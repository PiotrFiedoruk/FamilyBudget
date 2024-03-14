
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

from django.utils import timezone

from ..models import Budget, BudgetOperation

User = get_user_model()


class TestBudgetModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password', email='test@example.com')

    def test_create_budget(self):
        budget = Budget.objects.create(name='Test Budget', owner=self.user)

        saved_budget = Budget.objects.get(pk=budget.pk)

        self.assertEqual(saved_budget.name, 'Test Budget')
        self.assertEqual(saved_budget.owner, self.user)

    def test_shared_with(self):
        # Create another user for testing
        shared_user = User.objects.create_user(username='shared_user', password='shared_password',
                                               email='shared@example.com')

        budget = Budget.objects.create(name='Shared Budget', owner=self.user)

        # Share the budget with the shared user
        budget.shared_with.add(shared_user)

        saved_budget = Budget.objects.get(pk=budget.pk)

        # Check if the shared user is in the list of shared_with users
        self.assertIn(shared_user, saved_budget.shared_with.all())


class TestBudgetOperationModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password', email='test@example.com')
        cls.budget = Budget.objects.create(name='Test Budget', owner=cls.user)

    def test_create_budget_operation(self):
        # Create a budget operation
        operation = BudgetOperation.objects.create(
            category='Test Category',
            budget=self.budget,
            amount=Decimal('100.00'),
            date=timezone.now()
        )

        # Retrieve the budget operation from the database
        saved_operation = BudgetOperation.objects.get(pk=operation.pk)

        # Check if the retrieved budget operation matches the created one
        self.assertEqual(saved_operation.category, 'Test Category')
        self.assertEqual(saved_operation.budget, self.budget)
        self.assertEqual(saved_operation.amount, Decimal('100.00'))
