import datetime
import logging
from django.db import models
from django.db import transaction


# Create your models here.

class Brand(models.Model):
    name = models.CharField('Название', max_length=255)
    alias = models.CharField('Алиас', max_length=255)
    rating = models.IntegerField('Рейтинг', null=True, blank=True)
    popular = models.BooleanField('Популярный', null=True, blank=True)
    description = models.TextField('Описание',  null=True, blank=True)
    logo = models.FileField('Лого', null=True, blank=True, upload_to='brands/')            # Используем FileField т.к. ImageField не работает с .svg
    #logo_sm = models.ImageField(null=True, blank=True, upload_to='brands/')               # TODO image validation
    active = models.BooleanField('Активность', default=False, null=True, blank=True)


# Intermediate models

class BrandGroupConnManager(models.Manager):
    logger = logging.getLogger('advert.brand')

    def update_conn(self, brand, group):
        self.logger.info("Add group {}".format(group))
        if self.filter(brand=brand).exists():
            with transaction.atomic():
                conn = self.get(brand=brand)
                conn.group.add(group)
                conn.last_update = datetime.datetime.now()
                conn.save()
        else:
            with transaction.atomic():
                conn = BrandGroupConn(brand=brand)
                conn.last_update = datetime.datetime.now()
                conn.save()
                conn.group.add(group)

    def delete_conn(self, brand, group):
        self.logger.info("Remove group {}".format(group))
        if self.filter(brand=brand).exists():
            with transaction.atomic():
                conn = self.get(brand=brand)
                conn.group.remove(group)
                conn.last_update = datetime.datetime.now()
                conn.save()



class BrandGroupConn(models.Model):
    '''Связи с группами определяются автоматически из принадлежащих бренду продуктов'''
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ManyToManyField('product.Group')
    last_update = models.DateTimeField('Дата последнего обновления', default=None, null=True, blank=True)
    objects = BrandGroupConnManager()


class BrandCategoryConn(models.Model):
    '''Связи с категориями определяются автоматически из принадлежащих бренду продуктов'''
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ManyToManyField('product.Category')
    last_update = models.DateTimeField('Дата последнего обновления', default=None, null=True, blank=True)


