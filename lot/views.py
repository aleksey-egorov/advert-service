from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404

from lot.models import Lot, LotCatalog
from product.models import Category, Group
from brand.models import Brand
from geo.models import Region
from lot.forms import FilterForm, LotCreditForm, LotLeasingForm, LotRentForm
from supplier.forms import SupplierContactForm
from utils.form import FormHelper
from utils.context import Context

# Create your views here.

class CatalogLotsView(View):
    '''Основная страница каталога лотов'''

    def get(self, request, category=-1, pargroup=-1, group=-1):
        categories = Category.objects.filter(active=True).order_by("sorting")
        if Category.objects.filter(active=True, alias=category).exists():
            groups = Group.objects.filter(active=True, category=Category.objects.get(alias=category)).order_by('name')
        else:
            groups = Group.objects.filter(active=True).order_by('name')
        regions = Region.objects.filter(active=True).order_by('name')

        context = Context.get(request)
        page = request.POST.get('page')
        initial = {
            'region': context['vals']['region'].id,
            'category': category,
            'group': group,
            #'brand': brand
        }

        params = LotCatalog.prepare_params(initial, categories, groups)
        lot_list = Lot.objects.make_search(params)
        paginator = Paginator(lot_list, 12)

        try:
            lots = paginator.get_page(page)
        except PageNotAnInteger:
            lots = paginator.get_page(1)
        except EmptyPage:
            lots = paginator.get_page(page)

        form = FilterForm(regions, categories, groups)
        form.set_options(params)

        return render(request, "lot/catalog.html", {
            "form": form,
            "lots": lots,
            "context": context
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
        paginator = Paginator(lot_list, 12)

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
        recommended_lots = Lot.get_recommended(lot.id)

        form_contact = SupplierContactForm()
        form_contact.set_initial(lot.supplier.id)
        form_credit = LotCreditForm()
        form_credit.set_initial(lot.id)
        form_leasing = LotLeasingForm()
        form_leasing.set_initial(lot.id)
        form_rent = LotRentForm()
        form_rent.set_initial(lot.id)

        return render(request, "lot/lot.html", {
            "lot": lot,
            "form_contact": form_contact,
            "form_credit": form_credit,
            "form_leasing": form_leasing,
            "form_rent": form_rent,
            "recommended_lots": recommended_lots,
            "context": Context.get(request)
            #"message": "PARAMS={} ".format(params)
        })