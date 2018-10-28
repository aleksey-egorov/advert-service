from django.conf import settings

from product.models import Category, Group
from geo.models import Region


def get_main_menu():
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

def get_session_vals(request):
    vals = {}
    region = Region.objects.get(id=settings.DEFAULT_REGION)
    if request:
        try:
            if request.session['region'] > 0:
                region = Region.objects.get(id=request.session['region'])
            else:
                region = request.user.region
        except:
            pass
    vals['region'] = region
    return vals


class Context():

    @staticmethod
    def get(request=None):
        context = {
            'menu': get_main_menu(),
            'vals': get_session_vals(request)
        }
        return context