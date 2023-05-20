from django.views.generic import TemplateView
from rest_api.models import *
import json
# from django.utils.timezone import now
from django.views.generic.list import ListView
from django.utils import timezone
from django.contrib import messages
from datetime import datetime

diet_level = json.load(open("dashboard/data/diet_40_30_30.json"))
pecent_score = 0.15
health_percent_limit = 60


def calHealthScore(user_diet, user_diet_level):

    carbs_grams = user_diet_level["carbs_grams"]
    protein_grams = user_diet_level["protein_grams"]
    fat_grams = user_diet_level["fat_grams"]
    calorie_target = user_diet_level["calorie_target"]

    carbo_intake = user_diet["diet__total_carbohydrates__sum"]
    protein_intake = user_diet["diet__protein__sum"]
    fat_intake = user_diet["diet__total_fat__sum"]
    calorie_intake = user_diet["diet__calories__sum"]

    carbo_score_percent = carbs_grams * pecent_score
    protein_score_percent = protein_grams * pecent_score
    fat_score_percent = fat_grams * pecent_score
    calorie_score_percent = calorie_intake * pecent_score

    health_status = [
        carbo_intake > carbs_grams-carbo_score_percent,
        carbo_intake < carbs_grams+carbo_score_percent,
        protein_intake > protein_grams-protein_score_percent,
        protein_intake < protein_grams+protein_score_percent,
        fat_intake > fat_grams-fat_score_percent,
        fat_intake < fat_grams+fat_score_percent,
        calorie_intake > calorie_target-calorie_score_percent,
        calorie_intake < calorie_target+calorie_score_percent
    ]
    healthy_percent = round(
        (health_status.count(True)/len(health_status))*100, 2)
    if healthy_percent > health_percent_limit:
        return "healthy", healthy_percent, "green", health_status
    else:
        return "unhealthy", healthy_percent, "red", health_status


class Dashboard(TemplateView):
    template_name = "dashboard/dashboard.html"
    extra_context = {}

    def get(self, *args, **kwargs):
        user_id = 1
        user_obj = Person.objects.get(id=user_id)
        diet_data = user_obj.diet.filter(timestamp__date=datetime.now().date())
        if diet_data:
            # user_diet = diet_data.annotate(
            #     Sum("diet__calories"),
            #     Sum("diet__total_fat"),
            #     Sum("diet__protein"),
            #     Sum("diet__total_carbohydrates"),
            # )
            user_diet = {
                'diet__calories__sum': sum([float(i.replace("g", "")) for i in diet_data.values_list('diet__calories', flat=True)]),
                'diet__total_fat__sum': sum([float(i.replace("g", "")) for i in diet_data.values_list('diet__total_fat', flat=True)]),
                'diet__protein__sum': sum([float(i.replace("g", "")) for i in diet_data.values_list('diet__protein', flat=True)]),
                'diet__total_carbohydrates__sum': sum([float(i.replace("g", "")) for i in diet_data.values_list('diet__total_carbohydrates', flat=True)])
            }
        else:
            user_diet = {'diet__calories__sum': 0, 'diet__total_fat__sum': 0,
                         'diet__protein__sum': 0, 'diet__total_carbohydrates__sum': 0}

        user_vitamins = {
            "vitamin_a":sum([float(i.replace("%", "")) for i in diet_data.values_list('diet__vitamin_a', flat=True)]),
            "vitamin_c":sum([float(i.replace("%", "")) for i in diet_data.values_list('diet__vitamin_c', flat=True)]),
            "calcium":sum([float(i.replace("%", "")) for i in diet_data.values_list('diet__calcium', flat=True)]),
            "iron":sum([float(i.replace("%", "")) for i in diet_data.values_list('diet__iron', flat=True)]),
        }
        user_cholesterol = sum([float(i.replace("mg", "")) for i in diet_data.values_list('diet__cholesterol', flat=True)])

        user_diet_level = diet_level[user_obj.gender.lower()]
        user_diet = {k: round(v, 2) for k, v in user_diet.items()}
        total_vitamins_percent = sum(user_vitamins.values())
        user_vitamins = {k: round((v/total_vitamins_percent)*100, 2) if total_vitamins_percent else 0 for k, v in user_vitamins.items()}

        health_score, healthy_percent, color, health_status = calHealthScore(
            user_diet, user_diet_level)

        self.extra_context.update(user_diet)
        self.extra_context.update(user_diet_level)
        self.extra_context.update(user_vitamins)
        self.extra_context["cholesterol"] = round(user_cholesterol,2)
        self.extra_context["health_score"] = health_score
        self.extra_context["healthy_percent"] = healthy_percent
        self.extra_context["health_status"] = health_status
        self.extra_context["color"] = color
        self.extra_context["chartjs_4_data"] = [
            int(user_diet["diet__total_carbohydrates__sum"]),
            int(user_diet["diet__protein__sum"]),
            int(user_diet["diet__total_fat__sum"]),
        ]

        remaining_cal = user_diet_level["calorie_target"] - int(user_diet["diet__calories__sum"])
        remaining_cal = remaining_cal if remaining_cal >= 0 else 0
        self.extra_context["chartjs_5_data"] = [
            int(user_diet["diet__calories__sum"]),
            remaining_cal
        ]
        return super().get(*args, **kwargs)


class ViewMyDiet(ListView):
    template_name = "dashboard/viewmydiet.html"
    model = MyDiet
    extra_context = {}
    queryset = MyDiet.objects.all().order_by("-timestamp")
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        context['foods'] = FoodDatabase.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        intake = request.POST["intake"]
        user_obj = Person.objects.all().first()
        diet_obj = FoodDatabase.objects.get(name__iexact=intake)
        MyDiet.objects.create(user_id=user_obj,diet=diet_obj)
        count = MyDiet.objects.filter(user_id=user_obj,diet=diet_obj,timestamp__date=datetime.now().date()).count()
        messages.add_message(request, messages.SUCCESS, f"You have consumed {count} {intake} today")
        return super().get(request, *args, **kwargs)
