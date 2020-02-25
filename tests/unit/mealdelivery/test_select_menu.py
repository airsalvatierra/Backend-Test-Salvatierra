from datetime import datetime
import pytz

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.shortcuts import reverse
from freezegun import freeze_time

from comun.constants import ALLOW_VIEW_SELECTION
from mealdelivery.models import Menu, MenuEmployee, Employee
from mealdelivery.views import select_menu
from tests.utils import set_base_request


tz = pytz.timezone('America/Santiago')

class CreateMenuViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(CreateMenuViewTest, cls).setUpClass()
        cls.factory = RequestFactory()
        cls.url = reverse('mealdelivery:select_menu')
        cls.user = User.objects.create(
            username='angie',
            password='angie',
            is_superuser=True
        )
        cls.employee = Employee.objects.create(
            user=cls.user,
            country='Chile',
            slack_id='slack_id'
        )

    def setUp(self):

        self.data = {
            'menu_date': '24/02/2020',
            'option_selected': 'test',
        }

    @freeze_time('2020-02-24')
    def test_select_menu_get(self):
        request = self.factory.get(self.url)
        parsed_request = set_base_request(request, self.user)
        response = select_menu(parsed_request)

        self.assertEqual(response.status_code, 200)

    @freeze_time('2020-02-24')
    def test_select_menu_post(self):
        today = datetime.now(tz)
        ALLOW_VIEW_SELECTION.remove('angie')
        Menu.objects.create(
            menu_date=today,
            option1='test',
        )

        request = self.factory.post(self.url, self.data)
        parsed_request = set_base_request(request, self.user)
        response = select_menu(parsed_request)
        menu_selected = MenuEmployee.objects.get(menu_date=today)

        self.assertEqual(menu_selected.option_selected, 'test')
        self.assertEqual(response.status_code, 302)
