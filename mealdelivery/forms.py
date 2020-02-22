from django import forms

from .models import Menu


class MenuForm(forms.ModelForm):
    menu_date = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'data-provide': 'datepicker',
        'data-date-language': 'es',
    }), label='Date', required=False)

    class Meta:
        model = Menu
        fields = ['menu_date', 'option1', 'option2', 'option3', 'option4']
