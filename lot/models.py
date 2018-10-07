from django.db import models

# Create your models here.

class Currency(models.Model):
    name = models.CharField('Валюта', max_length=10)
    course = models.DecimalField('Курс', max_digits=5, decimal_places=2)

class Lot(models.Model):
    num = models.CharField('Код лота', max_length=10, default=None)
    name = models.CharField('Наименование', max_length=255, default='')
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

    def state_name(self):
        return "Новый" if self.new_prod_state == True else "б/у"

    def price_formatted(self):
        return "{:,}".format(self.price).replace(",", " ") + " " + self.currency.name

    def make_search(self, params):
        prod_state_map = {
            'all': None,
            'new': True,
            'used': False
        }
        filter_map = {}
        if not prod_state_map[params['prod_state']] == None:
            filter_map = {
                'new_prod_state': prod_state_map[params['prod_state']]
            }
        lot_list = Lot.objects.filter(**filter_map).order_by('-pub_date')
        return lot_list