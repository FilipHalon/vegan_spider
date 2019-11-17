from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework import generics, filters
from vegan_spider_app.models import Ingredient
from vegan_spider_app.serializers import IngredientDetailsSerializer


# Create your views here.

class IndexPage(View):

    def get(self, request):
        return render(request, 'index.html')


# class UserLogin(LoginView):
#     def redirect_to_index(self, request):
#         if not request.get('next'):


class IngredientDetails(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientDetailsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

