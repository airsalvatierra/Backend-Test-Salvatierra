from django.urls import path

from .views import CreateMenuView


app_name = 'mealdelivery'

urlpatterns = [
    path('newmenu', CreateMenuView.as_view(), name='newmenu'),
]
