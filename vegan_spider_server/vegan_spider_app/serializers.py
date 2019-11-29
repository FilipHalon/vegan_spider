from rest_framework import serializers

from vegan_spider_app.models import User, Ingredient, RecipeIngredient, Recipe, UserIngredient


class IngredientDetailSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='name')

    class Meta:
        model = Ingredient
        fields = ('id', 'text', 'photo')


class UserSerializer(serializers.ModelSerializer):
    ingredients = IngredientDetailSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'


class UserIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserIngredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class RecipeDetailSerializer(serializers.ModelSerializer):
    ingredients = IngredientDetailSerializer(
        many=True
    )
    ingredients_count = serializers.IntegerField(
        read_only=True
    )
    ingredients_included = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = '__all__'
