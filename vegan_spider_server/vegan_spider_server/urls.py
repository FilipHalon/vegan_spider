"""vegan_spider_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from vegan_spider_app.views import IngredientDetails, IndexPage, RecipeIngredients, UserLogin, RecipeDetails, \
    UserActionView, NewUserCreate

router = routers.SimpleRouter()
router.register(r'user', UserActionView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexPage.as_view(), name='index'),
    path('login/', UserLogin.as_view(), name='login'),
    path('new_user_create/', NewUserCreate.as_view(), name='new-user-create'),
    re_path(r'^(?P<user>.*)/password_change/',
            auth_views.PasswordChangeView.as_view(template_name="password_change.html")),
    re_path(r'^ingredients/$', IngredientDetails.as_view(), name='ingredients'),
    re_path(r'^recipe_ingredients/$', RecipeIngredients.as_view(), name="recipe-ingredients"),
    re_path(r'^recipe_details/$', RecipeDetails.as_view(), name="recipe-ingredients"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
