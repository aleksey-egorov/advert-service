"""Advert URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path

from django.contrib.auth import views as auth_views

from user.views import RegisterView, RegisterDoneView, ProfileView
from main.views import MainView
from lot.views import CatalogLotsView, CatalogLotsListView
from product.views import CatalogGroupsListView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='user/login.html', extra_context={}
    )),
    path('logout/', auth_views.LogoutView.as_view()),
    path('register/done/', RegisterDoneView.as_view()),
    path('register/', RegisterView.as_view()),
    path('user/profile/', ProfileView.as_view()),
    path('catalog/lots/list/', CatalogLotsListView.as_view()),
    path('catalog/lots/<str:category>/', CatalogLotsView.as_view()),
    path('catalog/lots/<str:category>/<str:group>/', CatalogLotsView.as_view()),
    path('catalog/lots/', CatalogLotsView.as_view()),
    path('catalog/groups/list/', CatalogGroupsListView.as_view()),
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
]
