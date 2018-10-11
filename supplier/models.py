from django.db import models

# Create your models here.

class Supplier(models.Model):
    '''Поставщик (офис или пункт продаж)'''
    name = models.CharField('Название', max_length=255)
    alias = models.CharField('Алиас', max_length=255)
    org = models.ForeignKey('Org', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField('Адрес')
    phone = models.CharField('Телефон', max_length=16)
    description = models.TextField('Описание',  null=True, blank=True)
    email = models.CharField('E-mail', max_length=60)
    url = models.CharField('Веб-сайт', max_length=120)
    rating = models.IntegerField('Рейтинг', null=True, blank=True)
    popular = models.BooleanField('Популярный', null=True, blank=True)
    active = models.BooleanField('Активность', default=False, null=True, blank=True)
    stat_lots_new = models.IntegerField('Статистика: новые лоты', null=True, blank=True)
    stat_lots_used = models.IntegerField('Статистика: б/у лоты', null=True, blank=True)

    def main_name(self):
        if not self.org == None:
            return self.org.name
        return self.name

    @property
    def stat_lots_total(self):
        return self.stat_lots_new + self.stat_lots_used

    def stat_lots_formatted(self):
        total = self.stat_lots_total
        if total < 1:
            return None
        elif total == 1:
            return str(total) + ' объявление'
        elif total > 1 and total < 5:
            return str(total) + ' объявления'
        elif total >= 5:
            return str(total) + ' объявлений'

class SupplierType(models.Model):
    name = models.CharField('Название', max_length=20)

class Org(models.Model):
    '''Головная организация-поставщик (или физлицо/ИП)'''
    name = models.CharField('Название', max_length=255)
    type = models.ForeignKey('SupplierType', on_delete=models.SET_NULL, null=True, blank=True)
    alias = models.CharField('Алиас', max_length=255)
    logo = models.ImageField(null=True, blank=True, upload_to='orgs/')
    phone = models.CharField('Телефон', max_length=16)
    url = models.CharField('Веб-сайт', max_length=120)
    description = models.TextField('Описание', null=True, blank=True)
    email = models.CharField('E-mail', max_length=60)
    popular = models.BooleanField('Популярный', null=True, blank=True)
    active = models.BooleanField('Активность', default=False, null=True, blank=True)