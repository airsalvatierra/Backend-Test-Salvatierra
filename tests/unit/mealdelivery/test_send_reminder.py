from datetime import datetime
import pytz

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.shortcuts import reverse
from freezegun import freeze_time
from mock import patch

from mealdelivery.views import SendReminder
from tests.utils import set_base_request


tz = pytz.timezone('America/Santiago')


class SendReminderViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(SendReminderViewTest, cls).setUpClass()
        cls.factory = RequestFactory()
        cls.url = reverse('mealdelivery:send')
        cls.user = User.objects.create(
            username='angie',
            password='angie',
            is_superuser=True
        )

    @freeze_time('2020-02-24')
    def setUp(self):
        self.data = {
            'exist': False,
            'today': datetime.now(tz),
            'sended': True,
            'errors': ''
        }

    @freeze_time('2020-02-24')
    @patch('mealdelivery.views.send_slack_reminder')
    def test_select_menu_get(self, mock):
        mock.return_value = 'ok'
        request = self.factory.get(self.url)
        parsed_request = set_base_request(request, self.user)
        response = SendReminder.as_view()(parsed_request)

        self.assertEqual(response.status_code, 200)
