import re
import os
import json
import logging
from django.utils import timezone
from django.db import models
from django.db import transaction
from django.conf import settings

from product.models import Product, Category, Group
from brand.models import Brand
from geo.models import Region
from supplier.models import Supplier, SupplierOrgGroupConn
from user.models import User
from utils.form import FormHelper


# Create your models here.

class Currency(models.Model):
    name = models.CharField('Валюта', max_length=10)
    course = models.DecimalField('Курс', max_digits=5, decimal_places=2)


class LotManager(models.Manager):
    logger = logging.getLogger('advert.lot')

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
            region = Region.objects.get(id=int(cleaned_data['region']))
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
                    add_date=timezone.now(),
                    main_image=None,
                    manuf_year=cleaned_data['manuf_year'],
                    region=region,
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
            self.logger.error(err)
            return False, err

    def update_lot(self, id, cleaned_data):
        try:
            product = Product.objects.get(active=True, id=int(cleaned_data['product']))
            currency = Currency.objects.get(id=int(cleaned_data['currency']))
            region = Region.objects.get(id=int(cleaned_data['region']))
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
                    upd_date=timezone.now(),
                    manuf_year=cleaned_data['manuf_year'],
                    region=region
                )
                upd_lot.save(update_fields=['name','product','price','currency','main_description','active','best',
                                            'new_prod_state','upd_date','manuf_year','region'])

                LotGallery.objects.update_gallery(upd_lot, json.loads(cleaned_data['image_filenames']))

                return True, None
        except Exception as err:
            self.logger.error(err)
            return False, err

    def make_search(self, params):
        filter_map = {}
        #st = ''

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

            #st += "KEY={} VAL={} {}".format(key, value, type(value))
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
        #msg = str(st) + "<br>FILTER_MAP={}".format(filter_map)
        return lot_list

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

    def update_conn(self, lot, old_group):
        self._update_lotbrand_conn(lot)
        self._update_lotgroup_conn(lot)
        self._update_lotcategory_conn(lot)
        self._update_suporggroup_conn(lot.supplier, (lot.product.group, old_group))


    def _update_lotbrand_conn(self, lot):
        brand = lot.product.brand
        if LotBrandConn.objects.filter(lot=lot).exists():
            with transaction.atomic():
                brand_conn = LotBrandConn.objects.get(lot=lot)
                brand_conn.brand = brand
                brand_conn.last_update = timezone.now()
                brand_conn.save()
        else:
            with transaction.atomic():
                brand_conn = LotBrandConn(
                    lot=lot,
                    brand=brand,
                    last_update=timezone.now()
                )
                brand_conn.save()

    def _update_lotgroup_conn(self, lot):
        group = lot.product.group
        if LotGroupConn.objects.filter(lot=lot).exists():
            with transaction.atomic():
                group_conn = LotGroupConn.objects.get(lot=lot)
                group_conn.brand = group
                group_conn.last_update = timezone.now()
                group_conn.save()
        else:
            with transaction.atomic():
                group_conn = LotGroupConn(
                    lot=lot,
                    group=group,
                    last_update=timezone.now()
                )
                group_conn.save()

    def _update_lotcategory_conn(self, lot):
        categories = lot.product.group.get_categories()
        if LotCategoryConn.objects.filter(lot=lot).exists():
            with transaction.atomic():
                cat_conn = LotCategoryConn.objects.get(lot=lot)
                cat_conn.last_update = timezone.now()
                cat_conn.save()
                for ct in categories:
                    cat_conn.category.add(ct)
        else:
            with transaction.atomic():
                cat_conn = LotCategoryConn(
                    lot=lot,
                    last_update=timezone.now()
                )
                cat_conn.save()
                for ct in categories:
                    cat_conn.category.add(ct)

    def _update_suporggroup_conn(self, sup, groups):
        if not sup == None:
            for some_group in groups:
                if not some_group == None and not sup.org == None:
                    suppliers_in_org = [sp.id for sp in Supplier.objects.filter(active=True, org=sup.org).all()]
                    products_in_group = [pr.id for pr in Product.objects.filter(active=True, group=some_group).all()]
                    if Lot.objects.filter(active=True, supplier__in=suppliers_in_org, product__in=products_in_group).exists():
                        SupplierOrgGroupConn.objects.update_conn(sup.org, some_group)
                    else:
                        SupplierOrgGroupConn.objects.delete_conn(sup.org, some_group)


class Lot(models.Model):
    num = models.CharField('Код лота', max_length=10, default=None, unique=True, null=True)
    name = models.CharField('Наименование', max_length=255,  null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey('geo.Region', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField('Цена', null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    main_description = models.TextField('Основное описание', default=None, null=True, blank=True)
    short_description = models.TextField('Краткое описание', default=None, null=True, blank=True)
    tech_description = models.TextField('Техническое описание', default=None, null=True, blank=True)
    alias = models.CharField('Алиас', max_length=255, default=None, unique=True, null=True)
    new_prod_state = models.BooleanField('Продукт новый или б/у', default=False, null=True, blank=True)
    add_date = models.DateTimeField('Дата добавления', default=None, null=True, blank=True)
    pub_date = models.DateTimeField('Дата публикации', default=None, null=True, blank=True)
    upd_date = models.DateTimeField('Дата последнего обновления', default=None, null=True, blank=True)
    act_date = models.DateTimeField('Дата окончания активности', default=None, null=True, blank=True)
    main_image = models.CharField('Главное фото', max_length=100, null=True, blank=True)
    manuf_year = models.IntegerField('Год выпуска', null=True, blank=True)
    tags = models.ManyToManyField('main.Tag')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    best = models.BooleanField('Рекомендованное предложение', default=False, null=True, blank=True)
    active = models.BooleanField('Активность', default=False, null=True, blank=True)

    objects = LotManager()
    logger = logging.getLogger('advert.lot')

    @property
    def state_name(self):
        return "Новый" if self.new_prod_state == True else "б/у"

    @property
    def product_name(self):
        return self.product.name

    @property
    def active_name(self):
        return "Да" if self.active == True else "Нет"

    @property
    def price_formatted(self):
        return "{:,}".format(self.price).replace(",", " ") + " " + self.currency.name

    @property
    def currency_name(self):
        return self.currency.name

    @property
    def supplier_name(self):
        return self.supplier.main_name

    @property
    def region_name(self):
        return self.region.name

    @property
    def categ_names_list(self):
        categories = Category.objects.filter(lotcategoryconn__lot=self).all()
        return ', '.join([x.name for x in categories])

    @property
    def tags_list(self):
        return ', '.join([tag.name for tag in self.tags.all()])

    @property
    def gallery_image_paths(self):
        image_paths = [x.big_image_path for x in LotGallery.objects.filter(lot=self).order_by('num').all()]
        return image_paths

    @property
    def full_name(self):
        return str(self.product.group.single_name) + ' ' + self.name + ' - ' + str(self.manuf_year) + ', ' + str(self.region_name)

    @staticmethod
    def get_recommended(id):
        # TODO: recommendation system
        lots = Lot.objects.filter(active=True).order_by('-pub_date')[:5]
        return lots

    def save(self, *args, **kwargs):
        old_group = self._lot_current_group()
        super().save(*args, **kwargs)
        Lot.objects.update_conn(self, old_group)

    def delete(self, *args, **kwargs):
        old_group = self._lot_current_group()
        super().delete(*args, **kwargs)
        #Lot.objects.update_conn(self, old_group)

    def _lot_current_group(self):
        cur_group = None
        if Lot.objects.filter(id=self.id).exists():
            cur_group = Lot.objects.get(id=self.id).product.group
        return cur_group


class LotCatalog():

    @staticmethod
    def prepare_params(initial, categories, groups):
        params = {
            'region': initial['region'],
            'category': FormHelper.get_option_id(categories, initial['category']),
            'group': FormHelper.get_option_id(groups, initial['group']),
        }
        return params


class LotGalleryManager(models.Manager):
    total_images = 12

    def get_images_forms(self, lot, upload_form, delete_form):
        lot_gallery = []

        for i in range(self.total_images):
            image_form = upload_form()
            image_form.set_initial(num=i, status='empty')
            lot_gallery.append({'num': i, 'type': 'empty', 'form': image_form})

        if not lot == None:
            gallery_images = self.filter(lot=lot)
            for im in gallery_images:
                del_form = delete_form()
                del_form.set_initial(num=im.num, status='old')
                lot_gallery[im.num] = {'num': im.num, 'type':'real', 'image': self.get_image_path(im.directory, im.big_image), 'form': del_form}

        return lot_gallery

    def save_tmp_image(self, image):
        filepath = os.path.join(settings.MEDIA_ROOT, 'lots', 'tmp', image.name )
        with open(filepath, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

    def update_gallery(self, lot, images):
        for image in images:
            if image['status'] == 'added':
                self._move_image_from_tmp(image['filename'])
                self._update_image(lot, image['num'], image['filename'])
            elif image['status'] == 'deleted':
                self._delete_image(lot, image['num'])
        self._update_main_image(lot)

    def _update_image(self, lot, num, filename):        # TODO: image saving path should be /lots/abc/ (abc - new subdirectory), not /lots/
        if self.filter(lot=lot, num=num).exists():
            with transaction.atomic():
                gallery = self.get(lot=lot, num=num)
                gallery.big_image = str(filename)
                gallery.save(update_fields=['big_image'])
        else:
            with transaction.atomic():
                gallery = LotGallery(
                    lot=lot,
                    num=num,
                    big_image=str(filename),
                    sorting=num,
                    active=True
                )
                gallery.save()

    def _move_image_from_tmp(self, filename):
        tmppath = os.path.join(settings.MEDIA_ROOT, 'lots', 'tmp', filename)
        realpath = os.path.join(settings.MEDIA_ROOT, 'lots', filename)
        os.rename(tmppath, realpath)

    def _move_image_from_location(self, source_path, filename):
        realpath = os.path.join(settings.MEDIA_ROOT, 'lots', filename)
        os.rename(source_path, realpath)

    def _delete_image(self, lot, num):
        if self.filter(lot=lot, num=num).exists():
            gallery = self.get(lot=lot, num=num)
            gallery.delete()

    def _update_main_image(self, lot):
        if self.filter(lot=lot).exists():
            first_image = self.filter(lot=lot).order_by('num')[0]
            if first_image.num >= 0:
                image = self.get(lot=lot, num=first_image.num)
                lot.main_image = self.get_image_path(image.directory, image.big_image)
                lot.save(update_fields=['main_image'])

    def get_image_path(self, subdir, file):
        if not subdir == None:
            return os.path.join(str(subdir), str(file))
        return str(file)


class LotGallery(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, null=True, blank=True)
    num = models.IntegerField('Номер', null=True, blank=True)
    directory = models.CharField('Папка', max_length=10, unique=False, null=True, blank=True)
    big_image = models.ImageField('Большое изображение', null=True, blank=True, upload_to='lots/')
    small_image = models.ImageField('Малое изображение', null=True, blank=True, upload_to='lots/')
    sorting = models.IntegerField('Сортировка', null=True, blank=True)
    active = models.BooleanField('Активность', default=True, null=True, blank=True)

    objects = LotGalleryManager()

    @property
    def big_image_path(self):
        return LotGallery.objects.get_image_path(self.directory, str(self.big_image))


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