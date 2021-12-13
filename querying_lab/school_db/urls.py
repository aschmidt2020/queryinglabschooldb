from django.urls import path
from . import views


app_name = 'lab'
urlpatterns = [
    path('', views.index, name="index"),
    path('one/', views.problem_one, name="one"),
    path('two/', views.problem_two, name="two"),
    path('three/', views.problem_three, name="three"),
    path('four/', views.problem_four, name="four"),
    path('five/', views.problem_five, name="five"),
    path('six/', views.problem_six, name="six"),
    path('bonus_one/', views.bonus_one, name="bonus_one"),
    path('bonus_two/', views.bonus_two, name="bonus_two")
]