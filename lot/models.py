import datetime
import re
import os
import json
from django.db import models
from django.db import transaction
from django.conf import settings

from product.models import Product, Category, Group
from brand.models import Brand
from supplier.models import Supplier
from user.models import User


# Create your models here.

class Currency(models.Model):
    name = models.CharField('Валюта', max_length=10)
    course = models.DecimalField('Курс', max_digits=5, decimal_places=2)


class LotManager(models.Manager):

    param_val_map = {
        'new_prod_state': {
            'all': None,
            'new': True,
            'used': False
        },
    }

    param_key_map = {
        'category': 'lotcategoryconn__category',
        'group': 'lotgroupconn__group',
        'brand': 'lotbrandconn__brand'
    }

    def add_lot(self, cleaned_data, user):
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

                LotGallery.objects.update_gallery(new_lot, json.loads(cleaned_data['image_filenames']))

                return True, None
        except Exception as err:
            return False, err

    def update_lot(self, id, cleaned_data):
        try:
            product = Product.objects.get(active=True, id=int(cleaned_data['product']))
            currency = Currency.objects.get(id=int(cleaned_data['currency']))
            with transaction.atomic():
                upd_lot = Lot(
                    id=id,
                    name=cleaned_data['name'],
                    product=product,
                    price=int(cleaned_data['price']),
                    currency=currency,
                    main_description=cleaned_data['main_description'],
                    active=cleaned_data['active'],
                    new_prod_state=self.param_val_map['new_prod_state'][cleaned_data['state']],
                    best=cleaned_data['best'],
                    upd_date=datetime.datetime.now(),
                    manuf_year=cleaned_data['manuf_year']
                )
                upd_lot.save(update_fields=['name','product','price','currency','main_description','active','best',
                                            'new_prod_state','upd_date','manuf_year'])

                LotGallery.objects.update_gallery(upd_lot, json.loads(cleaned_data['image_filenames']))

                return True, None
        except Exception as err:
            return False, err

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

        lot_list = self.filter(active=True).filter(**filter_map).order_by('-pub_date')
        msg = str(st) + "<br>FILTER_MAP={}".format(filter_map)
        return lot_list, msg

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

    objects = LotManager()

    def state_name(self):
        return "Новый" if self.new_prod_state == True else "б/у"

    def price_formatted(self):
        return "{:,}".format(self.price).replace(",", " ") + " " + self.currency.name

    @staticmethod
    def get_recommended(id):
        # TODO recommendation system
        lots = Lot.objects.filter(active=True).order_by('-pub_date')[:5]
        return lots

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_conns()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self._update_conns()

    def _update_conns(self):
        self._update_brand_conn()
        self._update_group_conn()
        self._update_category_conn()

    def _update_brand_conn(self):
        brand = Brand.objects.get(id=self.product.brand.id)
        if LotBrandConn.objects.filter(lot=self).exists():
            with transaction.atomic():
                brand_conn = LotBrandConn.objects.get(lot=self)
                brand_conn.brand = brand
                brand_conn.last_update = datetime.datetime.now()
                brand_conn.save()
        else:
            with transaction.atomic():
                brand_conn = LotBrandConn(
                    lot=self,
                    brand=brand,
                    last_update=datetime.datetime.now()
                )
                brand_conn.save()

    def _update_group_conn(self):
        group = Group.objects.get(id=self.product.group.id)
        if LotGroupConn.objects.filter(lot=self).exists():
            with transaction.atomic():
                group_conn = LotGroupConn.objects.get(lot=self)
                group_conn.brand = group
                group_conn.last_update = datetime.datetime.now()
                group_conn.save()
        else:
            with transaction.atomic():
                group_conn = LotGroupConn(
                    lot=self,
                    group=group,
                    last_update=datetime.datetime.now()
                )
                group_conn.save()

    def _update_category_conn(self):
        categories = self.product.group.get_categories()
        if LotCategoryConn.objects.filter(lot=self).exists():
            with transaction.atomic():
                cat_conn = LotCategoryConn.objects.get(lot=self)
                cat_conn.last_update = datetime.datetime.now()
                cat_conn.save()
                for ct in categories:
                    cat_conn.category.add(ct)
        else:
            with transaction.atomic():
                cat_conn = LotCategoryConn(
                    lot=self,
                    last_update=datetime.datetime.now()
                )
                cat_conn.save()
                for ct in categories:
                    cat_conn.category.add(ct)


class LotGalleryManager(models.Manager):

    def get_images_forms(self, lot, upload_form, delete_form):
        total_images = 12
        lot_gallery = []
        begin = 0
        if not lot == None:
            gallery_images = self.filter(lot=lot)
            for im in gallery_images:
                del_form = delete_form()
                del_form.set_initial(num=im.num, status='old')
                lot_gallery.append({'im': im, 'form': del_form})
            begin = len(lot_gallery)

        empty_images = []
        for i in range(total_images)[begin:]:
            image_form = upload_form()
            image_form.set_initial(num=i, status='empty')
            empty_images.append({'num': i, 'form': image_form})
        return lot_gallery, empty_images

    def save_tmp_image(self, image):
        filepath = os.path.join(settings.MEDIA_ROOT, 'lots', 'tmp', image.name )
        with open(filepath, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

    def update_gallery(self, lot, images):
        for image in images:
            if image['status'] == 'added':
                self.move_image_from_tmp(image['filename'])
                if self.filter(lot=lot, num=image['num']).exists():
                    lot_gallery = self.get(lot=lot, num=image['num'])
                    lot_gallery.image = image['filename']
                    lot_gallery.save(update_fields=['image'])
                else:
                    lot_gallery = LotGallery(
                        lot=lot,
                        num=image['num'],
                        image=image['filename'],
                        sorting=image['num'],
                        active=True
                    )
                    lot_gallery.save()

    def move_image_from_tmp(self, filename):
        os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")




class LotGallery(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, null=True, blank=True)
    num = models.IntegerField('Номер', null=True, blank=True)
    image = models.ImageField('Фото', null=True, blank=True, upload_to='lots/')
    sorting = models.IntegerField('Сортировка', null=True, blank=True)
    active = models.BooleanField('Активность', default=True, null=True, blank=True)

    objects = LotGalleryManager()



# Intermediate models

class LotBrandConn(models.Model):
    '''Значения полей определяются автоматически из поля Lot.product
        и нужны для облегчения поиска лотов
    '''
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey('brand.Brand', on_delete=models.CASCADE, null=True, blank=True)
    last_update = models.DateTimeField('Дата последнего обновления', default=None, null=True, blank=True)


class LotCategoryConn(models.Model):
    '''Значения полей определяются автоматически из поля Lot.product
            и нужны для облегчения поиска лотов
    '''
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ManyToManyField('product.Category')
    last_update = models.DateTimeField('Дата последнего обновления', default=None, null=True, blank=True)


class LotGroupConn(models.Model):
    '''Значения полей определяются автоматически из поля Lot.product
            и нужны для облегчения поиска лотов
    '''
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey('product.Group', on_delete=models.CASCADE, null=True, blank=True)
    last_update = models.DateTimeField('Дата последнего обновления', default=None, null=True, blank=True)