import uuid

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils import timezone

from comun.constants import COUNTRIES


# ***Fields from the Auth User Model***
# username
# first_name
# last_name
# email (Mandatory)
# password
# groups
# user_permissions
# is_staff
# is_active
# is_superuser
# last_login
# date_joined

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, choices=COUNTRIES)
    address = models.CharField(max_length=300, null=True, blank=True)
    # control fields
    created_at = models.DateTimeField(default=timezone.now)
    creation_user = models.CharField(max_length=250)
    last_modified = models.DateTimeField(null=True, blank=True)
    last_user_modified = models.CharField(
        max_length=250, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.user)


class Menu(models.Model):
    menu_date = models.DateField('Menu Date')
    uuid_url = models.UUIDField('UUID', default=uuid.uuid4, unique=True)
    option1 = models.CharField('Option 1', max_length=250)
    option2 = models.CharField(
        'Option 2',
        max_length=250,
        blank=True,
        null=True)
    option3 = models.CharField(
        'Option 3',
        max_length=250,
        blank=True,
        null=True)
    option4 = models.CharField(
        'Option 4',
        max_length=250,
        blank=True,
        null=True)
    # control fields
    created_at = models.DateTimeField(default=timezone.now)
    creation_user = models.CharField(max_length=250)
    last_modified = models.DateTimeField(null=True, blank=True)
    last_user_modified = models.CharField(
        max_length=250, blank=True, null=True)

    def __str__(self):
        return "Menu - {}".format(self.menu_date.strftime('%m/%d/%Y'))


class MenuEmployee(models.Model):
    employee = models.CharField(max_length=50)
    menu_date = models.DateField('Menu Date')
    option_selected = models.CharField(max_length=250)
    customization = models.CharField(max_length=500)
    # control fields
    created_at = models.DateTimeField(default=timezone.now)
    creation_user = models.CharField(max_length=250)
    last_modified = models.DateTimeField(null=True, blank=True)
    last_user_modified = models.CharField(
        max_length=250, blank=True, null=True)

    def __str__(self):
        return "{} - {} - {}".format(self.employee,
                                     self.menu_date.strftime('%m/%d/%Y'),
                                     self.option_selected)
