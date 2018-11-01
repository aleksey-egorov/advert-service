from django.shortcuts import render
from django.views.generic import View
from django.core import serializers
from django.shortcuts import get_object_or_404

from lot.models import Lot
from product.models import Group, ProductGallery, Product
from brand.forms import BrandForm
from utils.context import Context

# Create your views here.

class CatalogGroupsListView(View):

    def get(self, request):
        category = int(request.GET.get('category'))
        groups = Group.objects.filter(active=True, category=category)


        return render(request, "product/groups_json.html", {
            "groups": serializers.serialize('json', groups, fields=('name'))
        })


class ProductView(View):
    '''Страница продукта'''

    def get(self, request, alias):
        product = get_object_or_404(Product, alias=alias, active=True)
        lots = Lot.objects.filter(active=True, product=product).order_by('price')
        recom_products = Product.get_recommended(product.id)

        form_contact = BrandForm()
        form_contact.set_initial(product.brand.id)
      #  form_credit = LotCreditForm()
      #  form_credit.set_initial(lot.id)
      #  form_leasing = LotLeasingForm()
      #  form_leasing.set_initial(lot.id)
      #  form_rent = LotRentForm()
      #  form_rent.set_initial(lot.id)

        return render(request, "product/product.html", {
            "product": product,
            "lots": lots,
            "form_contact": form_contact,
            #"form_credit": form_credit,
            #"form_leasing": form_leasing,
            #"form_rent": form_rent,
            "recom_products": recom_products,
            "context": Context.get(request)
            # "message": "PARAMS={} ".format(params)
        })