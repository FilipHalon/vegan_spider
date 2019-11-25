from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Count, Sum, Case, When, Q, CharField
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import FormView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from vegan_spider_app.forms import NewUserCreateForm
from vegan_spider_app.models import Ingredient, RecipeIngredient, Recipe
from vegan_spider_app.serializers import IngredientDetailSerializer, RecipeIngredientSerializer, RecipeDetailSerializer, \
    UserSerializer


# Create your views here.

class IndexPage(View):

    def get(self, request):
        return render(request, 'index.html')


class UserLogin(LoginView):
    template_name = 'login.html'


# class NewUserCreate(FormView):
#     template_name = 'new_user_create.html'
#     form_class = NewUserCreateForm
#     success_url = '/'
#
#     def form_valid(self, form):
#         User.objects.create(username=form.cleaned_data['username'],
#                             email=form.cleaned_data['email'],
#                             password=User.set_password(form.cleaned_data['password']))
#         return super().form_valid(form)


# class NewUserCreate(FormView):
#     template_name = 'new_user_create.html'
#     form_class = UserCreationForm
#     success_url = '/'

class NewUserCreate(View):

    def get(self, request):
        form = NewUserCreateForm
        return render(request, 'new_user_create.html', {'form': form})


class UserActionView(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def current(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


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
        queried_ingredients = self.request.query_params.getlist('ingredients')
        queryset = super().get_queryset()
        queryset = queryset.annotate(ingredients_count=Count('ingredients', distinct=True))
        if queried_ingredients:
            # queryset = queryset.annotate(ingredients_included=Sum(
            #         Case(
            #             When(ingredients__in=queried_ingredients, then=1),
            #             output_field=CharField(),
            #         )
            #     )
            # )
            queryset = queryset.filter(ingredients__id__in=queried_ingredients).annotate(
                ingredients_included=Count(
                    'recipeingredient__ingredient', distinct=True
                )
            ).order_by()
        return queryset
