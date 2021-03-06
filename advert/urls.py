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
from django.conf.urls import url, include

from user.views import RegisterView, RegisterDoneView
from main.views import MainView, SearchView, TagView
from lot.views import CatalogLotsView, CatalogLotsListView, LotView
from product.views import CatalogGroupsListView, ProductView
from brand.views import BrandView
from supplier.views import SupplierOrgView, SupplierView
from article.views import ArticleView
from utils.context import Context



urlpatterns = [
    # Public pages
    path('catalog/lots/list/', CatalogLotsListView.as_view()),
    path('catalog/lots/<str:category>/', CatalogLotsView.as_view()),
    path('catalog/lots/<str:category>/<str:group>/', CatalogLotsView.as_view()),
    path('catalog/lots/<str:category>/<str:pargroup>/<str:group>/', CatalogLotsView.as_view()),
    path('catalog/lots/', CatalogLotsView.as_view()),
    path('catalog/groups/list/', CatalogGroupsListView.as_view()),
    path('lot/<str:alias>/', LotView.as_view()),
    path('product/<str:alias>/', ProductView.as_view()),
    path('brand/<str:alias>/', BrandView.as_view()),
    path('supplier/office/<str:alias>/', SupplierView.as_view()),
    path('supplier/<str:alias>/', SupplierOrgView.as_view()),
    path('article/<str:alias>/', ArticleView.as_view()),
    path('search/', SearchView.as_view()),
    path('tag/<str:tag>/', TagView.as_view()),

    # User
    path('register/done/', RegisterDoneView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html', extra_context={"context": Context.get()})),
    path('logout/', auth_views.LogoutView.as_view()),
    url(r'^user/', include('user.urls')),

    url(r'^acomp/', include('acomp.urls')),
    url(r'^sender/', include('sender.urls')),
    url(r'^api/', include('api.urls')),

    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
]
