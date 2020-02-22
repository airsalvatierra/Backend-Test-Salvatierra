import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','menumaker.settings')

import sys, csv
from itertools import cycle

import django
django.setup()
from django.utils import timezone

from django.contrib.auth.models import User
from mealdelivery.models import Employee

employees = [
    ['nora', 'nora@cornershopapp.com', 'Nora', 'Lauren', 'Chile'],
    ['alvin', 'alvin@cornershopapp.com', 'Alvin', 'Fuentes', 'Argentina'],
    ['robert', 'robert@cornershopapp.com', 'Robert', 'McQueen', 'Chile'],
    ['angie', 'angie@cornershopapp.com', 'Angie', 'Cruz', 'Chile'],
    ['yorki', 'yorki@cornershopapp.com', 'Yorki', 'Maluenda', 'Colombia'],
]

print('Creating Employees')

for i, emp in enumerate(employees):
    is_super = emp[0] == 'nora'
    user = User.objects.create(
        username=emp[0],
        email=emp[1],
        first_name=emp[2],
        last_name=emp[3],
        is_superuser=is_super
    )

    user.set_password(emp[0])
    user.save()

    employee = Employee.objects.create(
        user=user,
        country=emp[4]
    )

    print(i+1)
    print('User', user)
    print('Employee', employee)

print('Employees created')
