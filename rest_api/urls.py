from django.urls import path
from .views import *

app_name="api"

urlpatterns = [
    path('food/', FoodDatabaseView.as_view()),
    path('mydiet/', MyDietView.as_view()),
    path('food/<str:food_name>/', FoodDatabaseDetailView.as_view()),
]
