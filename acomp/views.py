from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from brand.models import Brand
from product.models import Product, Category
from utils.form import FormHelper

# Create your views here.

class BrandAcompView(View):
    ''' '''
    def get(self, request):
        q = request.GET.get('term')
        ct = int(request.GET.get('category'))
        brands = Brand.objects.filter(active=True, name__istartswith=q)
        if ct > 0:
            category = Category.objects.get(id=ct)
            brands = brands.filter(brandcategoryconn__category=category)
        br_options = FormHelper.make_acomp_options(brands)
        return JsonResponse(br_options, safe=False)

class ProductAcompView(View):
    ''' '''
    def get(self, request):
        q = request.GET.get('term')
        products = Product.objects.filter(active=True, name__istartswith=q)
        pr_options = FormHelper.make_acomp_options(products)
        return JsonResponse(pr_options, safe=False)

