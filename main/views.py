from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from lot.models import Lot
from article.models import Article
from brand.models import Brand
from supplier.models import Supplier

# Create your views here.

class MainView(View):

    def get(self, request):
        best_lots = Lot.objects.filter(active=True, best=True)[:10]
        new_lots = Lot.objects.filter(active=True).order_by('-pub_date')[:10]
        articles = Article.objects.filter(active=True).order_by('-date')[:3]
        brands = Brand.objects.filter(active=True, popular=True).order_by('-rating')[:10]
        suppliers = Supplier.objects.filter(active=True, popular=True).order_by('-rating')[:10]

        return render(request, "main/index.html", {
            "best_lots": best_lots,
            "new_lots": new_lots,
            "articles": articles,
            "brands": brands,
            "suppliers": suppliers
        })

