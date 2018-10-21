from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from main.models import Menu
from article.models import Article

# Create your views here.

class ArticleView(View):
    '''Основная страница статьи'''

    def get(self, request, alias):
        article = get_object_or_404(Article, active=True, alias=alias)

        return render(request, "article/article.html", {
            "article": article,
            "menu": Menu.get_main_menu()
        })