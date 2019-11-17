from rest_framework import serializers

from vegan_spider_app.models import Ingredient


class IngredientDetailsSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='name')

    class Meta:
        model = Ingredient
        fields = ('id', 'text', 'photo')
