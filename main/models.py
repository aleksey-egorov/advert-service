from django.db import models

from product.models import Category, Group

# Create your models here.

class Menu():

    def get_main_menu(self):
        cat_list = []
        categories = Category.objects.filter(active=True).order_by('sorting')
        for category in categories:
            groups = Group.objects.filter(active=True, category=category)
            gr_list = []
            for group in groups:
                gr_list.append({'name': group.name, 'url': str(category.alias) + '/' + str(group.get_url())})
            cat_dict = {
                'short_name': category.short_name,
                'alias': category.alias,
                'groups': gr_list
            }
            cat_list.append(cat_dict)
        return cat_list
