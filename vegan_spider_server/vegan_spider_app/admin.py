from django.contrib import admin

# Register your models here.
from vegan_spider_app.models import UserProfile, Ingredient, Recipe, Unit, RecipeIngredient

admin.site.register(UserProfile)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Unit)
admin.site.register(RecipeIngredient)
