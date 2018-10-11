from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404

from main.models import Menu
from brand.models import Brand
from product.models import Group, Product
from brand.forms import BrandForm

# Create your views here.

class BrandView(View):
    '''Основная страница бренда'''

    def get(self, request, alias):
        brand = get_object_or_404(Brand, alias=alias, active=True)
        groups = Group.objects.filter(active=True, brandgroupconn__brand=brand)
        popular_prods = Product.objects.filter(active=True, brand=brand)

        form = BrandForm()

        return render(request, "brand/brand.html", {
            "form": form,
            "brand": brand,
            "groups": groups,
            "popular_prods": popular_prods,
            "menu": Menu.get_main_menu(),
            #"message": "GROUPS={} ".format(groups)
        })
