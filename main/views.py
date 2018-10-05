from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from lot.models import Lot

# Create your views here.

class MainView(View):

    def get(self, request):
        lots_list = Lot.objects.order_by('-pub_date')[:10]

        return render(request, "main/index.html", {
            "lots": lots_list
        })

