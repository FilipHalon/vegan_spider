from django.contrib.auth.models import User
from rest_framework import serializers

from vegan_spider_app.models import Ingredient, RecipeIngredient, Recipe, UserIngredient


# class UserProfileSerializer(serializers.ModelSerializer):
#     # user = UserSerializer()
#     # ingredients = IngredientDetailSerializer(
#     #     many=True
#     # )
#     # id = serializers.IntegerField(source="user")
#
#     class Meta:
#         model = UserProfile
#         # fields = ('user', 'ingredients', 'photo')
#         # fields = ('id', 'photo')
#         fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # # photo = serializers.HyperlinkedRelatedField(
    # #     view_name='user-photo',
    # #     queryset=UserProfile.objects.all(),
    # #     lookup_url_kwarg={'user: user.pk'}
    # # )
    # ingredients = serializers.HyperlinkedRelatedField(
    #     view_name='user-ingredient',
    #     queryset=UserIngredient.objects.all(),
    #     # lookup_url_kwarg={'user: user.pk'}
    # )

    class Meta:
        model = User
        fields = '__all__'


class UserIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserIngredient
        fields = '__all__'


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
        # fields = ('name', 'photo', 'desc', 'link', 'ingredients', 'ingredients_count')

