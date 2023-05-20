from django.db import models

class FoodDatabase(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField()
    serving_size = models.CharField(max_length=100,null=True,blank=True)
    calories = models.CharField(max_length=100,null=True,blank=True)
    total_fat = models.CharField(max_length=100,null=True,blank=True)
    cholesterol = models.CharField(max_length=100,null=True,blank=True)
    sodium = models.CharField(max_length=100,null=True,blank=True)
    potassium  = models.CharField(max_length=100,null=True,blank=True)
    total_carbohydrates = models.CharField(max_length=100,null=True,blank=True)
    protein  = models.CharField(max_length=100,null=True,blank=True)
    vitamin_a  = models.CharField(max_length=100,null=True,blank=True)
    vitamin_c = models.CharField(max_length=100,null=True,blank=True)
    calcium = models.CharField(max_length=100,null=True,blank=True)
    iron = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.name} {self.serving_size}"

    
class Person(models.Model):
    name = models.CharField(max_length=140)
    gender = models.CharField(max_length=100,choices=(("Male","Male"),("Female","Female")))
    weight = models.FloatField(help_text="(kg)")
    height = models.FloatField(help_text="(cm)")
    age = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"


class MyDiet(models.Model):
    user_id = models.ForeignKey(Person,on_delete=models.CASCADE,related_name="diet")
    diet = models.ForeignKey(FoodDatabase,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user_id} - {self.diet}"
