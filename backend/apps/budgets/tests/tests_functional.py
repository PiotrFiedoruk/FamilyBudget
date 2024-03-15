from decimal import Decimal
import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from ..models import Budget, BudgetOperation

User = get_user_model()


class TestBudgetViewSet(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # created budget should appear on budget-details page
    def test_retrieve_budget(self):
        budget = Budget.objects.create(name='Test Budget', owner=self.user)
        response = self.client.get(f'/api/budgets/{budget.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Budget')

        # created budgets should appear on the list
    def test_budget_list(self):
        Budget.objects.create(name='Test Budget', owner=self.user)
        response = self.client.get('/api/budgets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'Test Budget')
        self.assertEqual(response.data['results'][0]['owner'], self.user.id)

    def test_budget_list_date_filter(self):
        budget = Budget.objects.create(name='Test Budget', owner=self.user)
        BudgetOperation.objects.create(category='Test Operation', budget=budget,
                                                          amount=Decimal('100.00'), date=datetime.date(2024, 3, 1))

        # any budget with budget operations with date within date range should appear on the list
        date_response = self.client.get('/api/budgets/?start_date=2024-03-01&end_date=2024-03-10')
        self.assertEqual(date_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(date_response.data['results']), 1)

        # if none of the related budget operations is not within date range budget should not appear on the list
        date_response = self.client.get('/api/budgets/?start_date=2024-04-01&end_date=2024-04-10') # 0 results
        self.assertEqual(date_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(date_response.data['results']), 0)

    def test_budget_list_search_filter(self):
        budget = Budget.objects.create(name='Test Budget', owner=self.user)
        BudgetOperation.objects.create(category='Test Operation', budget=budget,
                                                          amount=Decimal('100.00'), date=datetime.date(2024, 3, 1))

        # search query matches budget name
        search_response = self.client.get('/api/budgets/?search=Test Budget')
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_response.data['results']), 1)

        # search query doees not match
        search_response = self.client.get('/api/budgets/?search=Somename') # 0 results
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_response.data['results']), 0)


    def test_budget_list_owned_filter(self):
        other_user = User.objects.create_user(username='otheruser', password='testpassword')
        Budget.objects.create(name='Test Budget', owner=other_user)

        # no budgets owned or shared should return 0 results
        response = self.client.get('/api/budgets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

        # add owned budget
        Budget.objects.create(name='Test Budget', owner=self.user)

        # add ?type=owned filter, view should return owned budget
        response = self.client.get('/api/budgets/?type=owned')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  #

        #  general list view should return one owned budget
        response = self.client.get('/api/budgets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_budget_list_shared_filter(self):
        other_user = User.objects.create_user(username='otheruser', password='testpassword')
        other_budget = Budget.objects.create(name='Test Budget', owner=other_user)

        # no budgets owned or shared should return 0 results
        response = self.client.get('/api/budgets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

        # add shared budget
        other_budget.shared_with.add(self.user)
        other_budget.save()

        # add ?type=shared filter, view should return 1 shared budget
        response = self.client.get('/api/budgets/?type=shared')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # should return just one

        #  general list view should return one shared budget
        response = self.client.get('/api/budgets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class TestBudgetOperationViewSet(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.budget = Budget.objects.create(name='Test Budget', owner=self.user)

    def test_create_budget_operation(self):
        data = {
            'budget': self.budget.id,
            'category': 'Test Operation',
            'amount': '-100',
            "date": "2024-03-13",
        }
        response = self.client.post('/api/operations/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BudgetOperation.objects.count(), 1)
        self.assertEqual(BudgetOperation.objects.get().category, 'Test Operation')

    def test_retrieve_budget_operation(self):
        budget_operation = BudgetOperation.objects.create(category='Test Operation', budget=self.budget,
                                                          amount=Decimal('100.00'), date=datetime.date(2024, 3, 1))
        response = self.client.get(f'/api/operations/{budget_operation.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category'], budget_operation.category)
        self.assertEqual(response.data['date'], '2024-03-01')
        self.assertEqual(response.data['amount'], str(budget_operation.amount))

    def test_budget_operations_list(self):
        budget_operation = BudgetOperation.objects.create(category='Test Operation', budget=self.budget,
                                                          amount=Decimal('100.00'), date=datetime.date(2024, 3, 1))
        response = self.client.get(f'/api/operations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['category'], budget_operation.category)
        self.assertEqual(response.data['results'][0]['date'], '2024-03-01')
        self.assertEqual(response.data['results'][0]['amount'], str(budget_operation.amount))

    def test_budget_operations_list_date_filter(self):
        # any budgetoperations within date range and where budgets are owned by or shared with user should appear here
        budget = Budget.objects.create(name='Test Budget Dates', owner=self.user)
        BudgetOperation.objects.create(category='Test Operation', budget=budget,
                                                          amount=Decimal('100.00'), date=datetime.date(2024, 3, 1))
        # budget operation within dates
        date_response = self.client.get('/api/operations/?start_date=2024-03-01&end_date=2024-03-10')
        self.assertEqual(date_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(date_response.data['results']), 1)

        # budget operation outside of date range
        date_response = self.client.get('/api/operations/?start_date=2024-04-01&end_date=2024-04-10') # 0 results
        self.assertEqual(date_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(date_response.data['results']), 0)

    def test_budget_operations_list_search_filter(self):
        budget = Budget.objects.create(name='Test Budget Search', owner=self.user)
        BudgetOperation.objects.create(category='Test Operation', budget=budget,
                                                          amount=Decimal('100.00'), date=datetime.date(2024, 3, 1))

        # search term matches category
        search_response = self.client.get('/api/operations/?search=Test Operation')
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_response.data['results']), 1)

        # search term does not match category
        search_response = self.client.get('/api/operations/?search=Somename') # 0 results
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_response.data['results']), 0)
