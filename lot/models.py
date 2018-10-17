import datetime
import re
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
    num = models.CharField('Код лота', max_length=10, default=None, unique=True, null=True)
    name = models.CharField('Наименование', max_length=255,  null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField('Цена', null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    main_description = models.TextField('Основное описание', default=None, null=True, blank=True)
    short_description = models.TextField('Краткое описание', default=None, null=True, blank=True)
    tech_description = models.TextField('Техническое описание', default=None, null=True, blank=True)
    alias = models.CharField('Алиас', max_length=255, default=None, unique=True, null=True)
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

    param_val_map = {
        'new_prod_state': {
            'all': None,
            'new': True,
            'used': False
        },
    }

    param_key_map = {
        'defined_category': 'lotcategoryconn__category',
        'defined_group': 'lotgroupconn__group',
        'defined_brand': 'lotbrandconn__brand'
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
                value = self.param_val_map[key][params[key]]
            except:
                pass
            try:
                key = self.param_key_map[key]
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

    @staticmethod
    def get_recommended(id):
        # TODO recommendation system
        lots = Lot.objects.filter(active=True).order_by('-pub_date')[:5]
        return lots

    def add(self, cleaned_data, user):
        try:
            product = Product.objects.get(active=True, id=cleaned_data['product'])
            currency = Currency.objects.get(id=int(cleaned_data['currency']))
            with transaction.atomic():
                new_lot = Lot(
                    name=product.name,
                    product=product,
                    supplier=user.supplier,
                    price=int(cleaned_data['price']),
                    currency=currency,
                    main_description=cleaned_data['main_description'],
                    active=False,
                    new_prod_state=self.param_val_map['new_prod_state'][cleaned_data['state']],
                    best=False,
                    add_date=datetime.datetime.now(),
                    main_image=None,
                    manuf_year=cleaned_data['manuf_year'],
                    author=user
                )
                new_lot.save()
                alias, num = self._make_num_alias(new_lot.name, new_lot.id)
                new_lot.alias = alias
                new_lot.num = num
                new_lot.save()
                return True, None
        except Exception as err:
            return False, err

    def _make_num_alias(self, name, id):
        symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                   u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
        tr = {ord(a): ord(b) for a, b in zip(*symbols)}
        alias = name.translate(tr).lower()
        alias = re.sub('[\s\-]', '_', alias)
        alias = re.sub('[()]', '', alias)
        id_str = str(id)
        id_len = len(id_str)
        num = '0'*(6-id_len) + id_str
        alias += '_' + num
        return alias, num


class LotBrandConn(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey('brand.Brand', on_delete=models.SET_NULL, null=True, blank=True)              # Значения полей определяются автоматически из поля Lot.product
    last_update = models.DateTimeField('Дата последнего обновления', default=None, null=True, blank=True)   # и нужны для облегчения поиска лотов


class LotCategoryConn(models.Model):
    lot = models.ManyToManyField(Lot)
    category = models.ManyToManyField('product.Category')                                                   # Значения полей определяются автоматически из поля Lot.product
    last_update = models.DateTimeField('Дата последнего обновления', default=None, null=True, blank=True)   # и нужны для облегчения поиска лотов


class LotGroupConn(models.Model):
    lot = models.ManyToManyField(Lot)
    group = models.ManyToManyField('product.Group')                                                         # Значения полей определяются автоматически из поля Lot.product
    last_update = models.DateTimeField('Дата последнего обновления', default=None, null=True, blank=True)   # и нужны для облегчения поиска лотов