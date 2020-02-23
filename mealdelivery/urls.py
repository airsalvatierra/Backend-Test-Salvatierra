from django.urls import path

from .views import (CreateMenuView, ListMenusView, EditMenuView,
                    CreateEmployeeView, select_menu, MenuSelectedView,
                    SendReminderView)


app_name = 'mealdelivery'

urlpatterns = [
    path('new_menu/', CreateMenuView.as_view(), name='new_menu'),
    path('list_menus/', ListMenusView.as_view(), name='list_menus'),
    path('list_menus/<int:pk>/', EditMenuView.as_view(), name='edit_menu'),
    path('new_employee/', CreateEmployeeView.as_view(), name='new_employee'),
    path('select_menu/', select_menu, name='select_menu'),
    path('menus_selected/', MenuSelectedView.as_view(), name='menus_selected'),
    path('send_reminder/', SendReminderView.as_view(), name='send_reminder'),
]
