import datetime
from django.db import models
from django.db import transaction

from product.models import Product, Category, Group
from brand.models import Brand
from supplier.models import Supplier
from user.models import User

# Create your models here.

class Currency(models.Model):
    name = models.CharField('Валюта', max_length=10)
    course = models.DecimalField('Курс', max_digits=5, decimal_places=2)

class Lot(models.Model):
    num = models.CharField('Код лота', max_length=10, default=None)
    name = models.CharField('Наименование', max_length=255, default='')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField('Цена', null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    main_description = models.TextField('Основное описание', default=None)
    short_description = models.TextField('Краткое описание', default=None)
    tech_description = models.TextField('Техническое описание', default=None)
    alias = models.CharField('Алиас', max_length=255, default=None)
    active = models.BooleanField('Активность', default=False, null=True, blank=True)
    new_prod_state = models.BooleanField('Продукт новый или б/у', default=False, null=True, blank=True)
    best = models.BooleanField('Рекомендованное предложение', default=False, null=True, blank=True)
    add_date = models.DateTimeField('Дата добавления', default=None, null=True, blank=True)
    pub_date = models.DateTimeField('Дата публикации', default=None, null=True, blank=True)
    upd_date = models.DateTimeField('Дата последнего обновления', default=None, null=True, blank=True)
    act_date = models.DateTimeField('Дата окончания активности', default=None, null=True, blank=True)
    main_image = models.ImageField('Главное фото', null=True, blank=True, upload_to='lots/')
    manuf_year = models.IntegerField('Год выпуска', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    defined_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) # Значения полей defined_* определяются автоматически из поля product
    defined_group = models.ManyToManyField(Group)                                                    # и нужны для облегчения поиска лотов
    defined_brand = models.ManyToManyField(Brand)

    param_map = {
        'new_prod_state': {
            'all': None,
            'new': True,
            'used': False
        }
    }


    def state_name(self):
        return "Новый" if self.new_prod_state == True else "б/у"

    def price_formatted(self):
        return "{:,}".format(self.price).replace(",", " ") + " " + self.currency.name

    def make_search(self, params):
        filter_map = {}
        st = ''

        for key in params.keys():
            value = params[key]
            try:
                value = self.param_map[key][params[key]]
            except:
                pass
            st += "KEY={} VAL={} {}".format(key, value, type(value))
            if isinstance(value, str):
                if not value == '-1':
                    filter_map[key] = int(value)
            elif isinstance(value, int):
                if not value == -1:
                    filter_map[key] = value
            elif isinstance(value, list):
                if not '-1' in value and len(value) > 0:
                    filter_map[key + '__in'] = value
            elif isinstance(value, bool):
                filter_map[key] = value

        lot_list = Lot.objects.filter(**filter_map).order_by('-pub_date')
        msg = str(st) + "<br>FILTER_MAP={}".format(filter_map)
        return lot_list, msg

    def get_recommended(self, id):
        # TODO recommendation system
        lots = Lot.objects.filter(active=True).order_by('-pub_date')[:5]
        return lots

    @staticmethod
    def add(cleaned_data, user):
        try:
            product = Product.objects.get(active=True, id=cleaned_data['product'])
            with transaction.atomic():
                new_lot = Lot(
                    num='',
                    name='',
                    product=product,
                    supplier='',
                    price=cleaned_data['price'],
                    currency=cleaned_data['currency'],
                    main_description='',
                    alias='',
                    active=False,
                    new_prod_state=False,
                    best=False,
                    add_date=datetime.datetime.now(),
                    main_image=None,
                    manuf_year=cleaned_data['manuf_year'],
                    author=user
                )
                new_lot.save()
                return True, None
        except Exception as err:
            return False, err