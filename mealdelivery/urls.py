from django.urls import path

from .views import CreateMenuView, ListMenusView, EditMenuView


app_name = 'mealdelivery'

urlpatterns = [
    path('newmenu', CreateMenuView.as_view(), name='newmenu'),
    path('list_menus', ListMenusView.as_view(), name='list_menus'),
    path('list_menus/<int:pk>/', EditMenuView.as_view(), name='edit_menu'),
]
