from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

admin.site.register(Person)

@admin.register(MyDiet)
class MyDietAdmin(ImportExportModelAdmin):
    readonly_fields = ['timestamp']

@admin.register(FoodDatabase)
class FoodDatabaseAdmin(ImportExportModelAdmin):
    pass