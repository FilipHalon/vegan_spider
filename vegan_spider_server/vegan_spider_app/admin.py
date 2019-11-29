from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from vegan_spider_app.models import User, Ingredient, Recipe, Unit, RecipeIngredient, UserIngredient

admin.site.register(User, UserAdmin)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Unit)
admin.site.register(RecipeIngredient)
admin.site.register(UserIngredient)
