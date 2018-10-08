from django import forms

from lot.models import Lot
from product.models import Category, Group
from brand.models import Brand
from utils.form import make_options


class FilterForm(forms.Form):
    #class Meta:
    #    model = User

    categories = Category.objects.filter(active=True).order_by("sorting")
    cat_options = make_options(categories)
    groups = Group.objects.filter(active=True)
    gr_options = make_options(groups)
    brands = Brand.objects.filter(active=True)
    br_options = make_options(brands)

    defined_category = forms.ChoiceField(choices=cat_options, label='Категория')
    defined_group = forms.ChoiceField(choices=gr_options, label='Группа')
    defined_brand = forms.MultipleChoiceField(choices=br_options, label='Производитель')


    #def clean_login(self):
    #    login = self.cleaned_data['login']
    #    if User.objects.filter(username=login).exists():
    #        raise forms.ValidationError('User with login "' + login+ '" already exists')
    #    return login

