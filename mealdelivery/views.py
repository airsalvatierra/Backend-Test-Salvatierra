from datetime import datetime

from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .forms import MenuForm, UserForm, EmployeeForm, MenuEmployeeForm
from .models import Menu, MenuEmployee

# Login views


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if username == password:
                    return HttpResponseRedirect(reverse('change_password2'))
                return HttpResponseRedirect(reverse('home'))
            return HttpResponse("Account not active")
        print("Alguien a intentado entrar y fallo")
        print("Username: {} and password {}".format(username, password))
        return HttpResponse("Credenciales invalidas!")


@login_required
def home_page(request):
    if request.user.last_login is None:
        return HttpResponseRedirect(reverse('change_password2'))
    return render(request, 'index.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'You password has been changed!')
            return HttpResponseRedirect(reverse('home'))
        messages.error(request, 'Please, correct the errors mentioned!')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
    }

    return render(request, 'change_password.html', context)


def change_password_mandatory(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'You password has been changed!')
            logout(request)
        else:
            messages.error(request, 'Please, correct the errors mentioned!')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
    }

    return render(request, 'change_password.html', context)


# Meal Delivery views

class CreateMenuView(View):
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        registered = False

        form = MenuForm()

        context = {
            'form': form,
            'registered': registered
        }

        return render(request, 'mealdelivery/create_menu.html', context)

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request):
        registered = False

        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()

            registered = True

        context = {
            'form': form,
            'registered': registered
        }

        return render(request, 'mealdelivery/create_menu.html', context)

class ListMenusView(View):
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request):
        menus = Menu.objects.filter()

        context = {
            'menus': menus
        }

        return render(request, 'mealdelivery/list_menus.html', context)

class EditMenuView(View):
    @method_decorator(login_required(redirect_field_name=None))
    def get(self, request, pk):
        menu = Menu.objects.get(pk=pk)
        form = MenuForm(instance=menu)

        context = {
            'form': form
        }

        return render(request, 'mealdelivery/menu_update.html', context)

    @method_decorator(login_required(redirect_field_name=None))
    def post(self, request, pk):
        menu = Menu.objects.get(pk=pk)
        form = MenuForm(request.POST, instance=menu)

        if form.is_valid():
            form.save()

            messages.success(request, 'Menu updated')

            return redirect('mealdelivery:list_menus')

        context = {
            'form': form
        }

        return render(request, 'mealdelivery/menu_update.html', context)

class CreateEmployeeView(View):
    def get(self, request):
        userform = UserForm()
        employeeform = EmployeeForm()

        context = {
            'userform': userform,
            'employeeform': employeeform
        }

        return render(request, 'mealdelivery/create_employee.html', context)

    def post(self, request):
        userform = UserForm(request.POST or None)
        employeeform = EmployeeForm(request.POST or None)

        if userform.is_valid() and employeeform.is_valid():
            # create the user and the employee in the same time
            email = userform.cleaned_data.get('email')
            username = email.split('@')[0]
            user = userform.save(commit=False)
            user.username = username
            user.set_password(username)
            user.save()

            employee = employeeform.save(commit=False)
            employee.user = user
            employee.save()

            messages.success(request, 'Employee Created')

            return redirect('home')

        context = {
            'userform': userform,
            'employeeform': employeeform
        }

        return render(request, 'mealdelivery/create_employee.html', context)


@login_required
def select_menu(request):
    # check the limit to choose pass 11am
    today = datetime.now()
    date_time = datetime(today.year, today.month, today.day, 11)

    employee_menu = MenuEmployee.objects.filter(
        employee=request.user.username,
        menu_date=today
    )

    # if the employee already select the menu retur home
    if employee_menu.exists():
        messages.success(request, 'Yo already selected a menu for that day')
        return redirect('home')

    try:
        menu = Menu.objects.get(menu_date=today)
        # can_select = not today > date_time
        can_select = True
    except Menu.DoesNotExist:
        can_select = False
        form = MenuEmployeeForm()

        context = {
            'can_select': can_select,
            'form': form,
        }

        return render(request, 'mealdelivery/select_menu.html', context)

    # create choices from the existing menu
    choices = [
        (' ---------------------- ', ' ---------------------- '),
        (menu.option1, menu.option1)
    ]
    if menu.option2:
        choices.append((menu.option2, menu.option2))
    if menu.option3:
        choices.append((menu.option3, menu.option3))
    if menu.option4:
        choices.append((menu.option4, menu.option3))

    form = MenuEmployeeForm(
        request.POST or None,
        choices=choices,
        initial={
            'menu_date': menu.menu_date,
            'option_selected': choices,
            'employee': request.user.username
        }
    )

    if form.is_valid():
        MenuEmployee.objects.create(
            employee=request.user.username,
            menu_date=form.cleaned_data.get('menu_date'),
            option_selected=form.cleaned_data.get('option_selected'),
            customization=form.cleaned_data.get('customization')
        )
        messages.success(request, 'Menu Selected')
        return redirect('home')

    context = {
        'form': form,
        'can_select': True,
    }

    return render(request, 'mealdelivery/select_menu.html', context)

class MenuSelectedView(View):
    def get(self, request):
        menus = MenuEmployee.objects.all()

        context = {
            'menus': menus,
        }

        return render(request, 'mealdelivery/list_menus_selected.html', context)        
