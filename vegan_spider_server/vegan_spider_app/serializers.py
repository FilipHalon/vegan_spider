from rest_framework import serializers

from vegan_spider_app.models import Ingredient


class IngredientDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
