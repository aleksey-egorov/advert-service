from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404

from main.models import Menu
from product.models import Group
from lot.models import Lot
from supplier.models import SupplierOrg, Supplier
from supplier.forms import ContactForm

# Create your views here.

class SupplierOrgView(View):
    '''Основная страница организации-поставщика'''

    def get(self, request, alias):
        supplier_org = get_object_or_404(SupplierOrg, alias=alias, active=True)
        groups = Group.objects.filter(active=True, supplierorggroupconn__supplier_org=supplier_org)

        form = ContactForm()

        return render(request, "supplier/org.html", {
            "form": form,
            "org": supplier_org,
            "groups": groups,
            # "popular_prods": popular_prods,
            "menu": Menu.get_main_menu(),
            #"message": "GROUPS={} ".format(groups)
        })


class SupplierView(View):
    '''Cтраница офиса поставщика'''

    def get(self, request, alias):
        supplier = get_object_or_404(Supplier, alias=alias, active=True)
        best_lots = Lot.objects.filter(active=True, supplier=supplier, best=True)[:5]
        lots = Lot.objects.filter(active=True, supplier=supplier)

        form = ContactForm()

        return render(request, "supplier/supplier.html", {
            "form": form,
            "supplier": supplier,
            "best_lots": best_lots,
            "lots": lots,
            "menu": Menu.get_main_menu(),
            # "message": "GROUPS={} ".format(groups)
        })