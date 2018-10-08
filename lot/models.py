from django.db import models

from product.models import Product, Category, Group
from brand.models import Brand

# Create your models here.

class Currency(models.Model):
    name = models.CharField('Валюта', max_length=10)
    course = models.DecimalField('Курс', max_digits=5, decimal_places=2)

class Lot(models.Model):
    num = models.CharField('Код лота', max_length=10, default=None)
    name = models.CharField('Наименование', max_length=255, default='')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField('Цена', null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    main_description = models.TextField('Основное описание', default=None)
    short_description = models.TextField('Краткое описание', default=None)
    tech_description = models.TextField('Техническое описание', default=None)
    alias = models.CharField('Алиас', max_length=255, default=None)
    active = models.BooleanField('Активность', default=False, null=True, blank=True)
    new_prod_state = models.BooleanField('Продукт новый или б/у', default=False, null=True, blank=True)
    best = models.BooleanField('Рекомендованное предложение', default=False, null=True, blank=True)
    pub_date = models.DateTimeField('Дата публикации', default=None)
    upd_date = models.DateTimeField('Дата последнего обновления', default=None)
    active_date = models.DateTimeField('Дата окончания активности', default=None)
    main_image = models.ImageField('Главное фото', null=True, blank=True, upload_to='lots/')
    manuf_year = models.IntegerField('Год выпуска', null=True, blank=True)
    defined_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) # Значения полей defined_* определяются автоматически из поля product
    defined_group = models.ManyToManyField(Group)                                                    # и нужны для облегчения поиска лотов
    defined_brand = models.ManyToManyField(Brand)

    def state_name(self):
        return "Новый" if self.new_prod_state == True else "б/у"

    def price_formatted(self):
        return "{:,}".format(self.price).replace(",", " ") + " " + self.currency.name

    def make_search(self, params):
        param_map = {
            'new_prod_state': {
                'all': None,
                'new': True,
                'used': False
            }
        }
        filter_map = {}
        st = ''

        for key in params.keys():
            value = params[key]
            try:
                value = param_map[key][params[key]]
            except:
                pass
            st += "KEY={} VAL={} {}".format(key, value, type(value))
            if isinstance(value, str):
                if not value == '-1':
                    filter_map[key] = int(value)
            elif isinstance(value, list):
                if not '-1' in value and len(value) > 0:
                    filter_map[key + '__in'] = value
            elif isinstance(value, bool):
                filter_map[key] = value

        lot_list = Lot.objects.filter(**filter_map).order_by('-pub_date')
        msg = str(st) + "<br>FILTER_MAP={}".format(filter_map)
        return lot_list, msg