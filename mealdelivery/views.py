from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.utils.decorators import method_decorator

from .models import Menu
from .forms import MenuForm

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
        'form':form,
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
