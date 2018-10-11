from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404

from main.models import Menu
from supplier.models import Supplier

# Create your views here.


class SupplierView(View):
    '''Основная страница поставщика'''

    def get(self, request, alias):
        supplier = get_object_or_404(Supplier, alias=alias, active=True)
       # groups = Group.objects.filter(active=True, brandgroupconn__brand=brand)
       # popular_prods = Product.objects.filter(active=True, brand=brand)

        #form = BrandForm()

        return render(request, "supplier/supplier.html", {
           # "form": form,
           # "brand": brand,
           # "groups": groups,
           # "popular_prods": popular_prods,
            "menu": Menu.get_main_menu(),
            #"message": "GROUPS={} ".format(groups)
        })
