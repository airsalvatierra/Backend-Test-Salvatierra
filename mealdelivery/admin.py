from django.contrib import admin
from .models import Menu, MenuEmployee, Employee


class MenuAdmin(admin.ModelAdmin):
    fields = ['menu_date', 'option1', 'option2', 'option3', 'option4']
    list_display = ['menu_date', 'option1', 'option2', 'option3', 'option4']

class EmployeeAdmin(admin.ModelAdmin):
    fields = ['user', 'department', 'country', 'address']
    list_display = ['user', 'department', 'country', 'address']

class MenuEmployeeAdmin(admin.ModelAdmin):
    fields = ['employee', 'menu_date', 'option_selected', 'customization']
    list_display = ['employee', 'menu_date', 'option_selected']    


# Register your models here.
admin.site.register(Menu, MenuAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(MenuEmployee, MenuEmployeeAdmin)
