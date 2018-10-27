import datetime
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
    alias = models.CharField('Алиас', max_length=120, unique=True)
    description = models.TextField('Описание')
    pub_date = models.DateTimeField('Дата публикации', default=None)
    upd_date = models.DateTimeField('Дата последнего обновления', default=None)
    main_image = models.ImageField('Главное фото', null=True, blank=True, upload_to='products/')
    active = models.BooleanField('Активность', default=False, null=True, blank=True)

    objects = ProductManager()
    logger = logging.getLogger('advert.product')

    def save(self, *args, **kwargs):
        old_group = None
        if Product.objects.filter(id=self.id).exists():
            old_group = Product.objects.get(id=self.id).group
        super().save(*args, **kwargs)
        Product.objects.update_conn(self.brand, self.group, old_group)
        self.logger.info("Update prod conn {} {} {} ".format(self.brand, self.group, old_group))

    def delete(self, *args, **kwargs):
        old_group = None
        if Product.objects.filter(id=self.id).exists():
            old_group = Product.objects.get(id=self.id).group
        super().delete(*args, **kwargs)
        Product.objects.update_conn(self.brand, self.group, old_group)

