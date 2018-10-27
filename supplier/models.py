import logging
from django.utils import timezone
from django.db import models, transaction

# Create your models here.

class Supplier(models.Model):
    '''Поставщик (офис или пункт продаж)'''
    name = models.CharField('Название', max_length=255, null=False, blank=False)
    alias = models.CharField('Алиас', max_length=255, unique=True, null=False, blank=False)
    org = models.ForeignKey('SupplierOrg', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField('Адрес', null=True, blank=True)
    phone = models.CharField('Телефон', max_length=16, null=True, blank=True)
    description = models.TextField('Описание',  null=True, blank=True)
    email = models.CharField('E-mail', max_length=60, null=True, blank=True)
    url = models.CharField('Веб-сайт', max_length=120, null=True, blank=True)
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


class SupplierOrg(models.Model):
    '''Головная организация-поставщик (или физлицо/ИП)'''
    name = models.CharField('Название', max_length=255, null=False, blank=False)
    type = models.ForeignKey('SupplierType', on_delete=models.SET_NULL, null=True, blank=True)
    alias = models.CharField('Алиас', max_length=255, unique=True, null=False, blank=False)
    logo = models.FileField(null=True, blank=True, upload_to='orgs/')                           # Используем FileField т.к. ImageField не работает с svg
    phone = models.CharField('Телефон', max_length=16,null=True, blank=True)                    # TODO image validation
    url = models.CharField('Веб-сайт', max_length=120, null=True, blank=True)
    description = models.TextField('Описание', null=True, blank=True)
    email = models.CharField('E-mail', max_length=60, null=True, blank=True)
    rating = models.IntegerField('Рейтинг', null=True, blank=True)
    popular = models.BooleanField('Популярный', null=True, blank=True)
    tags = models.ManyToManyField('main.Tag')
    active = models.BooleanField('Активность', default=False, null=True, blank=True)


# Intermediate models

class SupplierOrgGroupConnManager(models.Manager):
    logger = logging.getLogger('advert.supplier')

    def update_conn(self, brand, group):
        if self.filter(brand=brand).exists():
            with transaction.atomic():
                conn = self.get(brand=brand)
                conn.group.add(group)
                conn.last_update = timezone.now()
                conn.save()
        else:
            with transaction.atomic():
                conn = SupplierOrgGroupConn(brand=brand)
                conn.last_update = timezone.now()
                conn.save()
                conn.group.add(group)

    def delete_conn(self, brand, group):
        if self.filter(brand=brand).exists():
            with transaction.atomic():
                conn = self.get(brand=brand)
                conn.group.remove(group)
                conn.last_update = timezone.now()
                conn.save()

class SupplierOrgGroupConn(models.Model):
    '''Связи с группами определяются автоматически из принадлежащих организации-поставщику лотов'''
    supplier_org = models.ForeignKey(SupplierOrg, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ManyToManyField('product.Group')
    last_update = models.DateTimeField('Дата последнего обновления', default=None, null=True, blank=True)
    objects = SupplierOrgGroupConnManager()
