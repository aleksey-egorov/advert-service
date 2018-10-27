from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404

from lot.models import Lot
from product.models import Category, Group
from brand.models import Brand
from geo.models import Region
from lot.forms import FilterForm, ContactForm
from utils.form import FormHelper
from utils.context import Context

# Create your views here.

class CatalogLotsView(View):
    '''Основная страница каталога лотов'''

    def get(self, request, category=-1, group=-1):
        categories = Category.objects.filter(active=True).order_by("sorting")
        groups = Group.objects.filter(active=True).order_by('name')
        brands = Brand.objects.filter(active=True).order_by('name')
        regions = Region.objects.filter(active=True).order_by('name')
        context = Context.get(request)

        params = {
            'region': context['vals']['region'].id,
            'category': FormHelper.get_option_id(categories, category),
            'group': FormHelper.get_option_id(groups, group),
        }
        lot_list = Lot.objects.make_search(params)

        form = FilterForm(regions, categories, groups, brands)
        form.set_options(params)

        return render(request, "lot/catalog.html", {
            "form": form,
            "lots": lot_list,
            "context": context,
            "message": "PARAMS={} ".format(params)
        })

class CatalogLotsListView(View):
    '''Обновление списка лотов (поиск), запрашивается через Ajax'''

    def __init__(self):
        self.params_keys = {
            'new_prod_state': 'bool',
            'category': 'int',
            'group': 'int',
            'brand': 'list',
            'region': 'int'
        }

    def post(self, request):

        page = request.POST.get('page')
        params = FormHelper.get_params_from_post(self.params_keys, request)

        lot_list = Lot.objects.make_search(params)
        paginator = Paginator(lot_list, 2)

        try:
            lots = paginator.get_page(page)
        except PageNotAnInteger:
            lots = paginator.get_page(1)
        except EmptyPage:
            lots = paginator.get_page(page)

        return render(request, "lot/list.html", {
            "lots": lots,
            "message": str(request.POST) + "PARAMS={} ".format(params)
        })

class LotView(View):
    '''Страница лота'''

    def get(self, request, alias):
        lot = get_object_or_404(Lot, alias=alias, active=True)
        form = ContactForm()
        recommended_lots = Lot.get_recommended(lot.id)

        return render(request, "lot/lot.html", {
            "lot": lot,
            "form": form,
            "recommended_lots": recommended_lots,
            "context": Context.get(request)
            #"message": "PARAMS={} ".format(params)
        })