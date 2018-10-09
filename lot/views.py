from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from main.models import Menu
from lot.models import Lot
from product.models import Category, Group
from brand.models import Brand
from lot.forms import FilterForm
from utils.form import FormHelper

# Create your views here.

class CatalogLotsView(View):
    '''Основная страница каталога лотов'''

    def get(self, request, category=-1, group=-1):
        categories = Category.objects.filter(active=True).order_by("sorting")
        groups = Group.objects.filter(active=True)
        brands = Brand.objects.filter(active=True)

        params = {
            'defined_category': FormHelper.get_option_id(categories, category),
            'defined_group': FormHelper.get_option_id(groups, group),
            #'defined_brand': FormHelper.get_option_id(categories, category)
        }
        lot_list, msg = Lot().make_search(params)

        form = FilterForm(categories, groups, brands)
        form.set_options(params)

        return render(request, "lot/catalog.html", {
            "form": form,
            "lots": lot_list,
            "menu": Menu().get_main_menu(),
            "message": "PARAMS={} ".format(params)
        })

class CatalogLotsListView(View):
    '''Обновление списка лотов (поиск) - запрашивается через Ajax'''

    def __init__(self):
        self.params_keys = {
            'new_prod_state': 'bool',
            'defined_category': 'int',
            'defined_group': 'int',
            'defined_brand': 'list'
        }

    def post(self, request):

        page = request.POST.get('page')
        params = FormHelper.get_params_from_post(self.params_keys, request)

        lot_list, msg = Lot().make_search(params)
        paginator = Paginator(lot_list, 20)

       # try:
       #     questions = paginator.get_page(page)
       # except PageNotAnInteger:
       #     questions = paginator.get_page(1)
       # except EmptyPage:
       #     questions = paginator.get_page(page)

        return render(request, "lot/list.html", {
            "lots": lot_list,
            "message": str(request.POST) + "PARAMS={} ".format(params) + msg
        })
