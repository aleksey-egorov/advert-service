from django import forms

from user.models import User
from utils.form import FormHelper
from product.models import Category, Product, Group
from lot.models import Currency, Lot
from brand.models import Brand
from geo.models import Region
from supplier.models import Supplier


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('avatar', )

    def set_initial(self, user):
        self.fields['phone'].initial = user.phone
        self.fields['region'].initial = user.region
        self.fields['email'].initial = user.email
        self.fields['supplier'].initial = user.supplier.id
        #self.fields['avatar'].initial = user.avatar

    email = forms.EmailField(label='E-mail', max_length=200)
    phone = forms.CharField(label='Телефон', max_length=16, required=False)
    avatar = forms.ImageField(label='Аватар', required=False)

    region_list = Region.objects.filter(active=True).all()
    region = forms.ChoiceField(label='Регион', choices=FormHelper.make_options(region_list, option_all=False))

    supplier_list = Supplier.objects.filter(active=True).all()
    supplier = forms.ChoiceField(label='Поставщик', choices=FormHelper.make_options(supplier_list, option_all=True))


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
    manuf_year = forms.IntegerField(label='Год выпуска', required=False)

    region_list = Region.objects.filter(active=True).order_by('name').all()
    region = forms.ChoiceField(label='Регион', choices=FormHelper.make_options(region_list, option_all=False))

    main_description = forms.CharField(label='Описание', widget=forms.Textarea, required=False)
    image_filenames = forms.CharField(widget=forms.HiddenInput)

    #TODO: extra fields and form validation


class LotEditForm(forms.Form):

    def set_options(self, id):
        lot = Lot.objects.get(id=id)
        product = Product.objects.get(id=lot.product.id)
        brand = Brand.objects.get(id=product.brand.id)
        group = Group.objects.get(id=product.group.id)
        categories = group.get_categories()
        state = "new" if lot.new_prod_state == True else "used"

        self.fields['name'].initial = lot.name
        self.fields['product'].initial = product.name
        self.fields['product_id'].initial = product.id
        self.fields['brand'].initial = brand.name
        self.fields['brand_id'].initial = brand.id
        self.fields['category'].initial = categories[0]
        self.fields['active'].initial = lot.active
        self.fields['best'].initial = lot.best
        self.fields['price'].initial = lot.price
        self.fields['currency'].initial = lot.currency.id
        self.fields['state'].initial = state
        self.fields['manuf_year'].initial = lot.manuf_year
        self.fields['region'].initial = lot.region.id
        self.fields['main_description'].initial = lot.main_description

    name = forms.CharField(label='Название лота')

    categories_list = Category.objects.filter(active=True).order_by("sorting")
    category = forms.ChoiceField(label='Категория', choices=FormHelper.make_options(categories_list))

    brand = forms.CharField(label='Бренд/марка')
    brand_id = forms.CharField(widget=forms.HiddenInput, required=False)
    product = forms.CharField(label='Модель')
    product_id = forms.CharField(widget=forms.HiddenInput, required=False)
    # TODO: replace brand and product with custom widgets

    active = forms.BooleanField(label='Лот активен', required=False)
    best = forms.BooleanField(label='В списке лучших', required=False)

    currency_list = Currency.objects.all()
    price = forms.IntegerField(label='Цена')
    currency = forms.ChoiceField(label='Валюта', choices=FormHelper.make_options(currency_list, option_all=False))

    state = forms.ChoiceField(label='Новый или б/у', choices=[("new", "Новый"), ("used", "б/у")])
    manuf_year = forms.IntegerField(label='Год выпуска', required=False)

    region_list = Region.objects.filter(active=True).order_by('name').all()
    region = forms.ChoiceField(label='Регион', choices=FormHelper.make_options(region_list, option_all=False))

    main_description = forms.CharField(label='Описание', widget=forms.Textarea, required=False)
    image_filenames = forms.CharField(widget=forms.HiddenInput)

    #TODO: extra fields and form validation



class LotDelForm(forms.Form):

    def set_initial(self, id):
        self.fields['lot_id'].initial = id

    lot_id = forms.IntegerField(widget=forms.HiddenInput)


class LotImageUploadForm(forms.Form):

    def set_initial(self, status, num):
        self.fields['num'].initial = num
        self.fields['status'].initial = status

    num = forms.CharField(widget=forms.HiddenInput, required=True)
    image = forms.ImageField(label=None)
    status = forms.CharField(widget=forms.HiddenInput, required=True)


class LotImageDelForm(forms.Form):

    def set_initial(self, status, num, filename=None):
        self.fields['num'].initial = num
        self.fields['status'].initial = status
        if not filename == None:
            self.fields['filename'].initial = filename

    num = forms.CharField(widget=forms.HiddenInput, required=True)
    filename = forms.CharField(widget=forms.HiddenInput, required=False)
    status = forms.CharField(widget=forms.HiddenInput, required=True)