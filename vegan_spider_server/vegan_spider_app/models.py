from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=256)
    photo = models.ImageField(blank=True)
    desc = models.CharField(max_length=512)
    link = models.CharField(max_length=256)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=16, blank=True)
    grams = models.IntegerField()

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.recipe}, {self.ingredient}, {self.quantity} {self.unit}"
