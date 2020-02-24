import os
from datetime import datetime
import pytz

from celery.decorators import task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from django.conf import settings
import slack

from mealdelivery.models import Employee, Menu
from .constants import ALLOW_VIEW_SELECTION

tz = pytz.timezone('America/Santiago')
logger = get_task_logger(__name__)


def check_if_is_supervisor(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return False
    return user.username in ALLOW_VIEW_SELECTION


@task(name="send_slack_reminder")
def send_slack_reminder(message, country=None):
    logger.info('Sending Reminders')
    # get employees
    if country:
        employees = Employee.objects.filter(country=country)
    else:
        employees = Employee.objects.all()

    # loop the employees and add reminder
    today = datetime.now(tz)
    date_time = datetime(today.year, today.month, today.day, 10)
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    if settings.DEBUG:
        time = 'in 30 seconds'
    else:
        time = datetime.timestamp(date_time)

    for employee in employees:
        response = client.reminders_add(
            user=employee.slack_id,
            time=time,
            text=message
        )
        if not response['ok']:
            logger.info('Error in employee: %s', employee.employee)

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
