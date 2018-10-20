from django import forms

from lot.models import Lot
from product.models import Category, Group
from brand.models import Brand
from utils.form import FormHelper


class FilterForm(forms.Form):

    def __init__(self, categories, groups, brands):
        super().__init__()
        self.categories = categories
        self.groups = groups
        self.brands = brands

    def set_options(self, params):
        self.fields['category'].choices = FormHelper.make_options(self.categories)
        self.fields['group'].choices = FormHelper.make_options(self.groups)
        self.fields['brand'].choices = FormHelper.make_options(self.brands)

        self.fields['category'].initial = params['category']
        self.fields['group'].initial = params['group']
        #self.fields['category'].initial = params['category']

    category = forms.ChoiceField(label='Категория')
    group = forms.ChoiceField(label='Группа')
    brand = forms.MultipleChoiceField(label='Производитель')

    #TODO: add extra fields and validation

    #def clean_login(self):
    #    login = self.cleaned_data['login']
    #    if User.objects.filter(username=login).exists():
    #        raise forms.ValidationError('User with login "' + login+ '" already exists')
    #    return login


class ContactForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=20)
    email = forms.EmailField(label='Email', max_length=200)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)

