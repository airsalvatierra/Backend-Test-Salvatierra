from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.shortcuts import reverse

from mealdelivery.models import Menu, Employee
from mealdelivery.views import CreateEmployeeView
from tests.utils import set_base_request


class EditMenuViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(EditMenuViewTest, cls).setUpClass()
        cls.factory = RequestFactory()
        cls.menu = Menu.objects.create(
            menu_date='2020-03-03',
            option1='test',
        )
        cls.url = reverse('mealdelivery:new_employee')
        cls.user = User.objects.create(
            username='angie',
            password='angie',
            is_superuser=True
        )

    def setUp(self):

        self.data = {
            'country': 'Chile',
            'slack_id': 'UA3K1MQQK',
            'email': 'nora@cornershopapp.com',
            'first_name': 'Nora',
            'last_name': 'Curry'
        }

    def test_create_employee_menu_get(self):
        request = self.factory.get(self.url)
        parsed_request = set_base_request(request, self.user)
        response = CreateEmployeeView.as_view()(parsed_request)

        self.assertEqual(response.status_code, 200)

    def test_create_menu_post(self):
        request = self.factory.post(self.url, self.data)
        parsed_request = set_base_request(request, self.user)
        response = CreateEmployeeView.as_view()(parsed_request)
        user = User.objects.get(username='nora')
        employee_created = Employee.objects.get(user=user)

        self.assertEqual(user.username, 'nora')
        self.assertEqual(employee_created.slack_id, 'UA3K1MQQK')
        self.assertEqual(employee_created.country, 'Chile')
        self.assertEqual(response.status_code, 302)

    def test_create_menu_post_invalid_data(self):
        self.data = {
            'menu_date': '03/03/2020',
            'option1': 'test michael jordan',
            'option2': 'test kobe bryant',
        }
        request = self.factory.post(self.url, self.data)
        parsed_request = set_base_request(request, self.user)
        response = CreateEmployeeView.as_view()(parsed_request)

        self.assertEqual(response.status_code, 200)
