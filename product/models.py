import os
import logging
from django.db import models
from django.db import transaction

from brand.models import Brand, BrandGroupConn, BrandCategoryConn

# Create your models here.

class Category(models.Model):
    name = models.CharField('Название', max_length=120)
    short_name = models.CharField('Короткое название', max_length=20)
    alias = models.CharField('Алиас', max_length=60, unique=True)
    sorting = models.IntegerField('Сортировка', null=True)
    main_image = models.ImageField('Главное фото', null=True, blank=True, upload_to='products/')
    active = models.BooleanField('Активность', default=False, null=True, blank=True)

    def has_products(self, brand):
        groups = Group.objects.filter(active=True, category=self).all()
        for group in groups:
            if Product.objects.filter(active=True, brand=brand, group=group).exists():
                return True
        return False


class Group(models.Model):
    name = models.CharField('Название', max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) # Группа-родитель всегда принадлежит одной категории
    parents = models.ManyToManyField('Group')                                                # Одна подгруппа может иметь несколько групп-родителей,
    alias = models.CharField('Алиас', max_length=120, unique=True)                           # а значит и несколько категорий
    single_name = models.CharField('Название (в единичном числе)', max_length=120, null=True, blank=True)
    active = models.BooleanField('Активность', default=False, null=True, blank=True)

    def get_url(self):
        par_url = ''
        if len(self.parents.all()) > 0:
            par = self.parents.all()[0]
            par_url = str(par.alias) + '/'
        return par_url + str(self.alias) + '/'

    def get_categories(self):
        if len(self.parents.all()) > 0:
            categories = [p.category.id for p in self.parents.all()]
        else:
            categories = [self.category.id]
        return categories


class ProductManager(models.Manager):

    def update_conn(self, brand, new_group, old_group):
        self._update_brandgroup_conn(brand, (new_group, old_group))
        self._update_brandcategory_conn(brand, (new_group, old_group))

    def _update_brandgroup_conn(self, brand, groups):
        for some_group in groups:
            if Product.objects.filter(active=True, brand=brand, group=some_group).exists():
                BrandGroupConn.objects.update_conn(brand, some_group)
            else:
                BrandGroupConn.objects.delete_conn(brand, some_group)

    def _update_brandcategory_conn(self, brand, groups):
        for some_group in groups:
            if not some_group == None:
                categories = some_group.get_categories()
                for categ_id in categories:
                    categ = Category.objects.get(id=categ_id)
                    if categ.has_products(brand):
                        BrandCategoryConn.objects.update_conn(brand, categ)
                    else:
                        BrandCategoryConn.objects.delete_conn(brand, categ)


class Product(models.Model):
    name = models.CharField('Название/Модель', max_length=120)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    alias = models.CharField('Алиас', max_length=120, unique=False)
    description = models.TextField('Описание', null=True, blank=True)
    pub_date = models.DateTimeField('Дата публикации', default=None, null=True, blank=True)
    upd_date = models.DateTimeField('Дата последнего обновления', default=None, null=True, blank=True)
    main_image = models.ImageField('Главное фото', null=True, blank=True, upload_to='products/')
    tech_description = models.TextField('Техническое описание', null=True, blank=True)
    popular = models.BooleanField('Популярный', null=True, blank=True)
    active = models.BooleanField('Активность', default=False, null=True, blank=True)

    objects = ProductManager()
    logger = logging.getLogger('advert.product')

    @property
    def brand_name(self):
        return self.brand.name

    @property
    def group_name(self):
        return self.group.name

    @property
    def gallery_image_paths(self):
        image_paths = [x.big_image_path for x in ProductGallery.objects.filter(product=self).order_by('num').all()]
        return image_paths

    @staticmethod
    def get_recommended(id):
        # TODO: recommendation system
        prod = Product.objects.get(id=id)
        products = Product.objects.filter(active=True, group=prod.group).order_by('name')[:5]
        return products

    def save(self, *args, **kwargs):
        old_group = None
        if Product.objects.filter(id=self.id).exists():
            old_group = Product.objects.get(id=self.id).group
        super().save(*args, **kwargs)
        Product.objects.update_conn(self.brand, self.group, old_group)

    def delete(self, *args, **kwargs):
        old_group = None
        if Product.objects.filter(id=self.id).exists():
            old_group = Product.objects.get(id=self.id).group
        super().delete(*args, **kwargs)
        Product.objects.update_conn(self.brand, self.group, old_group)


class ProductGalleryManager(models.Manager):

    def update_gallery(self, product, images):
        self._update_main_image(product)

    def _update_main_image(self, product):
        if self.filter(product=product).exists():
            first_image = self.filter(product=product).order_by('sorting')[0]
            if first_image.num >= 0:
                image = self.get(product=product, num=first_image.num)
                product.main_image = os.path.join(image.directory, str(image.big_image))
                product.save(update_fields=['main_image'])

    def get_image_path(self, subdir, file):
        if not subdir == None:
            return os.path.join(str(subdir), str(file))
        return str(file)


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    num = models.IntegerField('Номер изображения', null=True, blank=True)
    directory = models.CharField('Папка', max_length=10, unique=False, null=True, blank=True)
    big_image = models.ImageField('Большое изображение', null=True, blank=True, upload_to='products/')
    small_image = models.ImageField('Малое изображение', null=True, blank=True, upload_to='products/')
    sorting = models.IntegerField('Сортировка', null=True, blank=True)
    active = models.BooleanField('Активность', default=True, null=True, blank=True)

    objects = ProductGalleryManager()

    @property
    def big_image_path(self):
        return ProductGallery.objects.get_image_path(self.directory, str(self.big_image))