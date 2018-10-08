from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from main.models import Menu
from lot.models import Lot
from product.models import Category, Group

# Create your views here.

class CatalogLotsView(View):
    def get(self, request):
        categories = Category.objects.filter(active=True).order_by("sorting")
        groups = Group.objects.filter(active=True)

        return render(request, "lot/catalog.html", {
            "categories": categories,
            "groups": groups,
            "menu": Menu().get_main_menu()
        })

class CatalogLotsListView(View):
    def __init__(self):
        self.params_keys = ['new_prod_state','defined_category','defined_group']

    def post(self, request):

        page = request.POST.get('page')

        params = {}
        for key in self.params_keys:
            params[key] = request.POST.get(key)

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
            "message": str(request.POST) + msg
        })
