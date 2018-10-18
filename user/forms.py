from django import forms

from user.models import User
from utils.form import FormHelper
from product.models import Category, Product, Group
from lot.models import Currency, Lot
from brand.models import Brand


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','avatar',)


class RegisterForm(forms.Form):
    class Meta:
        model = User

    login = forms.CharField(label='Логин', max_length=200)
    email = forms.EmailField(label='E-mail', max_length=200)
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', max_length=200)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Пароль (повтор)', max_length=200)
    avatar = forms.ImageField(label='Аватар')

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(username=login).exists():
            raise forms.ValidationError('Пользователь с логином "' + login+ '" уже существует')
        return login


class LotAddForm(forms.Form):

    categories_list = Category.objects.filter(active=True).order_by("sorting")
    category = forms.ChoiceField(label='Категория', choices=FormHelper.make_options(categories_list))

    brand = forms.CharField(label='Бренд/марка')
    product = forms.CharField(label='Модель')

    currency_list = Currency.objects.all()
    price = forms.IntegerField(label='Цена')
    currency = forms.ChoiceField(label='Валюта', choices=FormHelper.make_options(currency_list, option_all=False))

    state = forms.ChoiceField(label='Новый или б/у', choices=[("new", "Новый"), ("used", "б/у")])
    manuf_year = forms.IntegerField(label='Год выпуска')

    main_description = forms.CharField(label='Описание', widget=forms.Textarea)

    #TODO: extra fields and form validation


class LotEditForm(forms.Form):

    def __init__(self, id):
        super().__init__()
        self.lot = Lot.objects.get(id=id)

    def set_options(self):
        product = Product.objects.get(id=self.lot.product.id)
        brand = Brand.objects.get(id=product.brand.id)
        group = Group.objects.get(id=product.group.id)
        categories = group.get_categories()

        self.fields['name'].initial = self.lot.name
        self.fields['product'].initial = product.name
        self.fields['product_id'].initial = product.id
        self.fields['brand'].initial = brand.name
        self.fields['brand_id'].initial = brand.id
        self.fields['category'].initial = categories[0]


        #self.fields['defined_group'].choices = FormHelper.make_options(self.groups)
        #self.fields['defined_brand'].choices = FormHelper.make_options(self.brands)

        #self.fields['defined_category'].initial = params['defined_category']
        #self.fields['defined_group'].initial = params['defined_group']


    name = forms.CharField(label='Название лота')

    categories_list = Category.objects.filter(active=True).order_by("sorting")
    category = forms.ChoiceField(label='Категория', choices=FormHelper.make_options(categories_list))

    brand = forms.CharField(label='Бренд/марка')
    brand_id = forms.CharField(widget=forms.HiddenInput)
    product = forms.CharField(label='Модель')
    product_id = forms.CharField(widget=forms.HiddenInput)

    currency_list = Currency.objects.all()
    price = forms.IntegerField(label='Цена')
    currency = forms.ChoiceField(label='Валюта', choices=FormHelper.make_options(currency_list, option_all=False))

    state = forms.ChoiceField(label='Новый или б/у', choices=[("new", "Новый"), ("used", "б/у")])
    manuf_year = forms.IntegerField(label='Год выпуска')

    main_description = forms.CharField(label='Описание', widget=forms.Textarea)

    #TODO: extra fields and form validation