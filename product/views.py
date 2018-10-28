from django.shortcuts import render
from django.views.generic import View
from django.core import serializers

from product.models import Group, ProductGallery, Product

# Create your views here.

class CatalogGroupsListView(View):

    def get(self, request):
        category = int(request.GET.get('category'))
        groups = Group.objects.filter(active=True, category=category)


        return render(request, "product/groups_json.html", {
            "groups": serializers.serialize('json', groups, fields=('name'))
        })
