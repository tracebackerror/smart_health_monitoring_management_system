from rest_framework import serializers
from .models import *

class FoodDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodDatabase
        fields = '__all__'

class MyDietDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyDiet
        fields = '__all__'



