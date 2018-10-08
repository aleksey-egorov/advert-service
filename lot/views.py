from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from main.models import Menu
from lot.models import Lot
from product.models import Category, Group
from brand.models import Brand
from lot.forms import FilterForm

# Create your views here.

class CatalogLotsView(View):
    def get(self, request):
        categories = Category.objects.filter(active=True).order_by("sorting")
        groups = Group.objects.filter(active=True)
        brands = Brand.objects.filter(active=True)
        form = FilterForm()

        return render(request, "lot/catalog.html", {
            "categories": categories,
            "groups": groups,
            "brands": brands,
            "form": form,
            "menu": Menu().get_main_menu()
        })

class CatalogLotsListView(View):
    def __init__(self):
        self.params_keys = {
            'new_prod_state': 'bool',
            'defined_category': 'int',
            'defined_group': 'int',
            'defined_brand': 'list'
        }

    def post(self, request):

        page = request.POST.get('page')
        params = {}
        for key in self.params_keys:
            if self.params_keys[key] in ('bool', 'int'):
                params[key] = request.POST.get(key)
            elif self.params_keys[key] == 'list':
                params[key] = request.POST.getlist(key)

        lot_list, msg = Lot().make_search(params)
        paginator = Paginator(lot_list, 20)

        try:
            questions = paginator.get_page(page)
        except PageNotAnInteger:
            questions = paginator.get_page(1)
        except EmptyPage:
            questions = paginator.get_page(page)

        return render(request, "lot/list.html", {
            "lots": lot_list,
            "message": str(request.POST) + "PARAMS={} ".format(params) + msg
        })
