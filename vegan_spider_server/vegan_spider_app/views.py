from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework import generics, filters
from vegan_spider_app.models import Ingredient, RecipeIngredient, Recipe
from vegan_spider_app.serializers import IngredientDetailSerializer, RecipeIngredientSerializer, RecipeDetailSerializer


# Create your views here.

class IndexPage(View):

    def get(self, request):
        return render(request, 'index.html')


class UserLogin(LoginView):
    redirect_field_name = 'index'
    template_name = 'login.html'


class IngredientDetails(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientDetailSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class RecipeIngredients(generics.ListAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer


class RecipeDetails(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
