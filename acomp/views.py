from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from brand.models import Brand
from product.models import Product
from utils.form import FormHelper

# Create your views here.

class BrandAcompView(View):
    ''' '''
    def get(self, request):
        q = request.GET.get('term')
        brands = Brand.objects.filter(active=True, name__istartswith=q)
        br_options = FormHelper.make_acomp_options(brands)
        return JsonResponse(br_options, safe=False)

class ProductAcompView(View):
    ''' '''
    def get(self, request):
        q = request.GET.get('term')
        products = Product.objects.filter(active=True, name__istartswith=q)
        pr_options = FormHelper.make_acomp_options(products)
        return JsonResponse(pr_options, safe=False)

