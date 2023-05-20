from django.urls import path
from .views import *

app_name="dashboard"

urlpatterns = [
    path('', Dashboard.as_view()),
    path('view-my-diet', ViewMyDiet.as_view()),
]
