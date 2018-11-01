from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from brand.models import Brand
from product.models import Product, Category
from geo.models import Region
from utils.form import FormHelper

# Create your views here.

class BrandAcompView(View):
    ''' '''
    def get(self, request):
        q = request.GET.get('term')
        ct = 0
        if not request.GET.get('category') == None:
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

class RegionListAcompView(View):
    ''' '''
    def get(self, request):
        regions = Region.objects.filter(active=True).order_by('name')
        reg_options = FormHelper.make_acomp_options(regions)
        return JsonResponse(reg_options, safe=False)

class SessionAcompView(View):
    ''' '''
    def get(self, request):
        region_id = int(request.GET.get('region'))
        region = Region.objects.get(id=region_id)
        if region:
            request.session['region'] = region.id
            return JsonResponse({'region': region.name}, safe=False)