from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.shortcuts import reverse

from comun.constants import ALLOW_VIEW_SELECTION
from mealdelivery.models import Menu
from mealdelivery.views import CreateMenuView
from tests.utils import set_base_request


class CreateMenuViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(CreateMenuViewTest, cls).setUpClass()
        cls.factory = RequestFactory()
        cls.url = reverse('mealdelivery:new_menu')
        cls.user = User.objects.create(
            username='angie',
            password='angie',
            is_superuser=True
        )

    def setUp(self):

        self.data = {
            'menu_date': '03/03/2020',
            'option1': 'test',
        }

    def test_create_menu_get(self):
        request = self.factory.get(self.url)
        parsed_request = set_base_request(request, self.user)
        response = CreateMenuView.as_view()(parsed_request)

        self.assertEqual(response.status_code, 200)

    def test_create_menu_get_not_permited(self):
        ALLOW_VIEW_SELECTION.remove('angie')
        request = self.factory.get(self.url)
        parsed_request = set_base_request(request, self.user)
        response = CreateMenuView.as_view()(parsed_request)

        self.assertEqual(response.status_code, 302)

    def test_create_menu_post(self):
        ALLOW_VIEW_SELECTION.append('angie')
        request = self.factory.post(self.url, self.data)
        parsed_request = set_base_request(request, self.user)
        response = CreateMenuView.as_view()(parsed_request)
        menu_created = Menu.objects.get(menu_date='2020-03-03')

        self.assertEqual(menu_created.option1, 'test')
        self.assertEqual(response.status_code, 200)
