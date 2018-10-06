from django.db import models

# Create your models here.

class Brand(models.Model):
    name = models.CharField('Название', max_length=255)
    alias = models.CharField('Алиас', max_length=255)
    rating = models.IntegerField('Рейтинг', null=True, blank=True)
    popular = models.BooleanField('Популярный', null=True, blank=True)
    description = models.TextField('Описание',  null=True, blank=True)
    small_logo = models.ImageField(null=True, blank=True, upload_to='brands/')
    big_logo = models.ImageField(null=True, blank=True, upload_to='brands/')
    active = models.BooleanField('Активность', default=False, null=True, blank=True)