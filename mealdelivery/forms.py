from datetime import datetime

from django import forms
from django.contrib.auth.models import User

from .models import Employee, Menu


class MenuForm(forms.ModelForm):
    menu_date = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'data-provide': 'datepicker',
        'data-date-language': 'en',
        'autocomplete': 'off'
    }), label='Date', required=True)

    class Meta:
        model = Menu
        fields = ['menu_date', 'option1', 'option2', 'option3', 'option4']

    def clean(self):
        if not self.instance.pk:
            menu_date = self.cleaned_data.get('menu_date')
            menu_date = datetime(
                menu_date.year,
                menu_date.month,
                menu_date.day,
                10)
            if menu_date < datetime.now():
                raise forms.ValidationError(
                    'You cannot create a menu for the pass, you have until '
                    '10am of today or pass that to create a menu')

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

    def clean(self):
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
        fields = ['user', 'department', 'country', 'address', 'slack_id']

class MenuEmployeeForm(forms.Form):
    menu_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'data-provide': 'datepicker',
                'data-date-language': 'en',
                'autocomplete': 'off'
            }
        ),
        required=False,
    )

    option_selected = forms.ChoiceField(
        label='Options',
        widget=forms.Select(),
    )

    employee = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(
            attrs={
                'hidden': 'true'}))

    customization = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    def __init__(self, *args, choices=None, **kwargs):
        super(MenuEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['menu_date'].disabled = True
        if choices:
            self.fields['option_selected'].choices = choices
