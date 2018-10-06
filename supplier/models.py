from django.db import models

# Create your models here.

class Supplier(models.Model):
    name = models.CharField('Название', max_length=255)
    alias = models.CharField('Алиас', max_length=255)
    address = models.TextField('Адрес')
    phone = models.CharField('Телефон', max_length=16)
    description = models.TextField('Описание',  null=True, blank=True)
    email = models.CharField('E-mail', max_length=60)
    url = models.CharField('Веб-сайт', max_length=120)
    rating = models.IntegerField('Рейтинг', null=True, blank=True)
    popular = models.BooleanField('Популярный', null=True, blank=True)
    active = models.BooleanField('Активность', default=False, null=True, blank=True)
