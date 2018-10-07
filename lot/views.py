from django.shortcuts import render
from django.views.generic import View

from main.models import Menu

# Create your views here.

class CatalogLotsView(View):

    def get(self, request):

        return render(request, "lot/catalog.html", {
            "menu": Menu().get_main_menu()
        })
