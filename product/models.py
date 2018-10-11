from django.db import models

from brand.models import Brand

# Create your models here.

class Category(models.Model):
    name = models.CharField('Название', max_length=120)
    short_name = models.CharField('Короткое название', max_length=20)
    alias = models.CharField('Алиас', max_length=60, unique=True)
    sorting = models.IntegerField('Сортировка')
    main_image = models.ImageField('Главное фото', null=True, blank=True, upload_to='products/')
    active = models.BooleanField('Активность', default=False, null=True, blank=True)

class Group(models.Model):
    name = models.CharField('Название', max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) # Группа-родитель всегда принадлежит одной категории
    parents = models.ManyToManyField('Group')                                                # Одна подгруппа может иметь несколько групп-родителей
    alias = models.CharField('Алиас', max_length=120, unique=True)
    active = models.BooleanField('Активность', default=False, null=True, blank=True)

    def get_url(self):
        par_url = ''
        if len(self.parents.all()) > 0:
            par = self.parents.all()[0]
            par_url = par + '/'
        return par_url + str(self.alias) + '/'

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