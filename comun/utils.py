import os
from datetime import datetime
import pytz

from django.contrib.auth.models import User
from django.conf import settings
import slack

from mealdelivery.models import Employee, Menu
from .constants import ALLOW_VIEW_SELECTION

tz = pytz.timezone('America/Santiago')


def check_if_is_supervisor(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return False
    return user.username in ALLOW_VIEW_SELECTION


def send_slack_reminder(message, country=None):
    # get employees
    if country:
        employees = Employee.objects.filter(country=country)
    else:
        employees = Employee.objects.all()

    # loop the employees and add reminder
    today = datetime.now(tz)
    date_time = datetime(today.year, today.month, today.day, 10)
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
    errors = []
    for employee in employees:
        response = client.reminders_add(
            user=employee.slack_id,
            time=datetime.timestamp(date_time),
            text=message
        )
        if not response['ok']:
            errors.append(employee.employee)

    if errors:
        return errors
    return 'ok'


def get_slack_reminder_message(today):
    try:
        menu = Menu.objects.get(menu_date=today)
    except Menu.DoesNotExist:
        return None

    if settings.DEBUG:
        url = "http://127.0.0.1:8000/menu/{}".format(menu.uuid_url)
    else:
        url = "https://nora.cornershop.io/menu/{}".format(menu.uuid_url)

    message = 'Remeber to choose your meal {}'.format(url)

    return message
