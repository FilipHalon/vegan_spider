from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    photo = models.ImageField(blank=True, upload_to='profile_photos')
    ingredients = models.ManyToManyField('Ingredient', through="UserIngredient")


class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    photo = models.ImageField(blank=True, upload_to='ingredients')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=256)
    photo = models.ImageField(blank=True, upload_to='recipes')
    desc = models.CharField(max_length=512)
    link = models.CharField(max_length=256)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=16, blank=True)
    # grams = models.IntegerField()

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, blank=True)
    quantity = models.FloatField(blank=True)

    def __str__(self):
        return f"{self.recipe}, {self.ingredient}, {self.quantity} {self.unit}"


class UserIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}, {self.ingredient}, {self.quantity} {self.unit}"
