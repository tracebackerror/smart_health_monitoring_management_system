from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status as http_status
from django.shortcuts import render

# from rest_framework.views import APIView


class FoodDatabaseView(generics.ListAPIView):
    queryset = FoodDatabase.objects.all()
    serializer_class = FoodDatabaseSerializer


class FoodDatabaseDetailView(generics.RetrieveAPIView):
    queryset = FoodDatabase.objects.all()
    serializer_class = FoodDatabaseSerializer
    lookup_url_kwarg = "food_name"
    lookup_field = "name__iexact"

    def post(self, request, *args, **kwargs):
        response = {}
        try:
            user_id = int(request.POST["user_id"])
            user_obj = Person.objects.get(id=user_id)
            diet_obj = FoodDatabase.objects.get(name__iexact=self.kwargs[self.lookup_url_kwarg])
            MyDiet.objects.create(user_id=user_obj,diet=diet_obj)
            response["details"] = "Record created successfully"
            status = http_status.HTTP_201_CREATED
        except Exception as e:
            response["details"] = str(e)
            status = http_status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(response,status=status)


class MyDietView(generics.ListAPIView):
    queryset = MyDiet.objects.all()
    serializer_class = MyDietDatabaseSerializer


def index(request):
    """View function for home page of site."""

    context = {

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)