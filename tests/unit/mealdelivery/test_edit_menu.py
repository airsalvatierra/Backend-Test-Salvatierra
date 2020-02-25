from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.shortcuts import reverse

from comun.constants import ALLOW_VIEW_SELECTION
from mealdelivery.models import Menu
from mealdelivery.views import EditMenuView
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
        cls.url = reverse('mealdelivery:edit_menu',
                          kwargs={'pk': cls.menu.pk})
        cls.user = User.objects.create(
            username='angie',
            password='angie',
            is_superuser=True
        )

    def setUp(self):

        self.data = {
            'menu_date': '03/03/2020',
            'option1': 'test michael jordan',
            'option2': 'test kobe bryant',
        }

    def test_edit_menu_get(self):
        request = self.factory.get(self.url)
        parsed_request = set_base_request(request, self.user)
        response = EditMenuView.as_view()(parsed_request, self.menu.pk)

        self.assertEqual(response.status_code, 200)

    def test_edit_menu_post(self):
        ALLOW_VIEW_SELECTION.append('angie')
        request = self.factory.post(self.url, self.data)
        parsed_request = set_base_request(request, self.user)
        response = EditMenuView.as_view()(parsed_request, self.menu.pk)
        edited_menu = Menu.objects.get(menu_date='2020-03-03')

        self.assertEqual(edited_menu.option1, 'test michael jordan')
        self.assertEqual(edited_menu.option2, 'test kobe bryant')
        self.assertEqual(response.status_code, 302)
