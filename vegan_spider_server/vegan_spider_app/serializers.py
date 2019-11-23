from rest_framework import serializers

from vegan_spider_app.models import Ingredient, RecipeIngredient, Recipe


class IngredientDetailSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='name')

    class Meta:
        model = Ingredient
        fields = ('id', 'text', 'photo')


class RecipeIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class RecipeDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = '__all__'

