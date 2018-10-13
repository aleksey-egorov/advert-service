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
        self.fields['defined_category'].choices = FormHelper.make_options(self.categories)
        self.fields['defined_group'].choices = FormHelper.make_options(self.groups)
        self.fields['defined_brand'].choices = FormHelper.make_options(self.brands)

        self.fields['defined_category'].initial = params['defined_category']
        self.fields['defined_group'].initial = params['defined_group']
        #self.fields['defined_category'].initial = params['defined_category']

    defined_category = forms.ChoiceField(label='Категория')
    defined_group = forms.ChoiceField(label='Группа')
    defined_brand = forms.MultipleChoiceField(label='Производитель')

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


