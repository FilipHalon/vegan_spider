from django.contrib.auth.views import LoginView
from django.db.models import Count, Sum, Case, When, Q, CharField
from django.shortcuts import render, get_object_or_404
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
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
    # queryset = Recipe.objects.annotate(ingredients_count=Count('ingredients'))
    serializer_class = RecipeDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ingredients']

    def get_queryset(self):
        queryset = super().get_queryset()
        queried_ingredients = self.request.query_params.getlist('ingredients')
        queryset = queryset.annotate(ingredients_count=Count('ingredients', distinct=True))
        if queried_ingredients is not None:
            queryset = queryset.annotate(ingredients_in=Sum(
                    Case(
                        When(ingredients__in=queried_ingredients, then=1),
                        output_field=CharField(),
                    )
                )
            )
        return queryset
