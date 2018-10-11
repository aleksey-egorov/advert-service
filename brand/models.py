from django.db import models

# Create your models here.

class Brand(models.Model):
    name = models.CharField('Название', max_length=255)
    alias = models.CharField('Алиас', max_length=255)
    rating = models.IntegerField('Рейтинг', null=True, blank=True)
    popular = models.BooleanField('Популярный', null=True, blank=True)
    description = models.TextField('Описание',  null=True, blank=True)
    logo = models.FileField('Лого', null=True, blank=True, upload_to='brands/')            # Используем FileField т.к. ImageField не работает с svg
    #logo_sm = models.ImageField(null=True, blank=True, upload_to='brands/')               # TODO image validation
    active = models.BooleanField('Активность', default=False, null=True, blank=True)


class BrandGroupConn(models.Model):                                                        # Связи с группами определяются автоматически из принадлежащих бренду продуктов
    brand = models.ManyToManyField(Brand)                                                  # и нужны для облегчения поиска групп по брендам
    group = models.ManyToManyField('product.Group')
    last_update = models.DateTimeField('Дата последнего обновления', default=None, null=True, blank=True)

