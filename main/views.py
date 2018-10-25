from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from lot.models import Lot
from article.models import Article
from brand.models import Brand
from supplier.models import SupplierOrg
from main.models import Tag
from utils.context import Context

# Create your views here.

class MainView(View):
    '''Главная страница'''
    def get(self, request):
        best_lots = Lot.objects.filter(active=True, best=True)[:10]
        new_lots = Lot.objects.filter(active=True).order_by('-pub_date')[:10]
        articles = Article.objects.filter(active=True).order_by('-date')[:3]
        brands = Brand.objects.filter(active=True, popular=True).order_by('-rating')[:10]
        supplier_orgs = SupplierOrg.objects.filter(active=True, popular=True).order_by('-rating')[:10]

        return render(request, "main/index.html", {
            "best_lots": best_lots,
            "new_lots": new_lots,
            "articles": articles,
            "brands": brands,
            "supplier_orgs": supplier_orgs,
            "context": Context.get(request)
        })


class SearchView(View):
    '''Страница поиска'''
    def get(self, request):
        query = request.GET.get('q')

        lots = Lot.objects.filter(active=True).filter(Q(name__icontains=query)).order_by('-pub_date')[:20]              # TODO: more fields to search
        articles = Article.objects.filter(active=True).filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-date')[:20]
        suppliers = SupplierOrg.objects.filter(active=True).filter(Q(name__icontains=query)).order_by('-rating')[:20]
        brands = Brand.objects.filter(active=True).filter(Q(name__icontains=query)).order_by('-rating')[:20]

        return render(request, "main/search.html", {
            "lots": lots,
            "articles": articles,
            "suppliers": suppliers,
            "brands": brands,
            "query": query,
            "context": Context.get(request)
        })


class TagView(View):

    def get(self, request, tag):
        tag = str(tag).strip()
        if Tag.objects.filter(name=tag).exists():
            tag_elem = Tag.objects.get(name=tag)
            articles = Article.objects.filter(active=True, tags=tag_elem).order_by('-date')[:20]
            suppliers = SupplierOrg.objects.filter(active=True, tags=tag_elem).order_by('-rating')[:20]
            brands = Brand.objects.filter(active=True, tags=tag_elem).order_by('-rating')[:20]

            return render(request, "main/tag.html", {
                "articles": articles,
                "suppliers": suppliers,
                "brands": brands,
                "query": "tag:{}".format(tag),
                "context": Context.get(request)
                #"message": suppliers
            })
