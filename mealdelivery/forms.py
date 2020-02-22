from django import forms
from django.contrib.auth.models import User

from .models import Employee, Menu


class MenuForm(forms.ModelForm):
    menu_date = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'data-provide': 'datepicker',
        'data-date-language': 'en',
    }), label='Date', required=True)

    class Meta:
        model = Menu
        fields = ['menu_date', 'option1', 'option2', 'option3', 'option4']

    def clean_menu_date(self):
        menu_date = self.cleaned_data.get('menu_date')
        menu = Menu.objects.filter(menu_date=menu_date).exists()
        if menu:
            raise forms.ValidationError(
                "A menu already exist for this date")


class UserForm(forms.ModelForm):
    username = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(
            attrs={
                'hidden': 'true'}))
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'is_superuser']

    def clean_email(self):
        mail = self.cleaned_data.get('email')
        mail = mail.split('@')[0]
        username = User.objects.filter(username=mail).exists()
        if username:
            raise forms.ValidationError('This username already exists')



class EmployeeForm(forms.ModelForm):
    user = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(
            attrs={
                'hidden': 'true'}))

    class Meta:
        model = Employee
        fields = ['user', 'department', 'country', 'address']
