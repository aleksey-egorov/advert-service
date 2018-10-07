from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from main.models import Menu
from lot.models import Lot

# Create your views here.

class CatalogLotsView(View):
    def get(self, request):

        return render(request, "lot/catalog.html", {
            "menu": Menu().get_main_menu()
        })


class CatalogLotsListView(View):
    def post(self, request):

        page = request.POST.get('page')

        params = {
            'prod_state': request.POST.get('prod_state')
        }
        lot_list = Lot().make_search(params)
        paginator = Paginator(lot_list, 20)

        try:
            questions = paginator.get_page(page)
        except PageNotAnInteger:
            questions = paginator.get_page(1)
        except EmptyPage:
            questions = paginator.get_page(page)

        return render(request, "lot/list.html", {
            "lots": lot_list,
            "message": request.POST
        })
