from django.test import TestCase
from django.utils import timezone

from brand.models import Brand
from lot.models import Lot, Currency
from product.models import Product, Group, Category
from supplier.models import Supplier, SupplierOrg
from user.models import User

# Supplier unit tests.

class SupplierTestCase(TestCase):

   def setUp(self):
      SupplierOrg.objects.create(id=1, active=True, name="Организация 1")
      Supplier.objects.create(id=11, name="Поставщик 1", active=True, org=SupplierOrg.objects.get(id=1))
      self.user = User.objects.create(username='test', password='test',  supplier=Supplier.objects.get(id=11))
      Brand.objects.create(id=11, name="KAMAZ")
      Category.objects.create(id=11, name="Строительная техника", sorting=1, alias='str', active=True)
      Category.objects.create(id=12, name="Дорожная техника", sorting=1, alias='dor', active=True)
      category = Category.objects.get(id=11)
      category2 = Category.objects.get(id=12)
      Group.objects.create(id=11, name="Самосвалы", category=category, active=True, alias='group_11')
      Group.objects.create(id=12, name="Грузовые автомобили", category=category2, active=True, alias='group_12')
      Currency.objects.create(id=11, name="RUR", course=1)

   def test_suporggroup_conn(self):
      brand = Brand.objects.get(id=11)
      group = Group.objects.get(id=11)
      group2 = Group.objects.get(id=12)
      Product.objects.create(id=11, name="KAMAZ-6521", brand=brand, group=group,
                             alias='kamaz-6521', description='test',
                             pub_date=timezone.now(), active=True, upd_date=timezone.now())
      Product.objects.create(id=12, name="KAMAZ-6522", brand=brand, group=group2,
                             alias='kamaz-6522', description='test',
                             pub_date=timezone.now(), active=True, upd_date=timezone.now())
      Lot.objects.create(id=11, num="000001", name="КАМАЗ-6520", product=Product.objects.get(id=11), price=2000000,
                         currency=Currency.objects.get(id=11), supplier=self.user.supplier, author=self.user, active=True)
      Lot.objects.create(id=12, num="000002", name="КАМАЗ-6522", product=Product.objects.get(id=12), price=1000000,
                         currency=Currency.objects.get(id=11), supplier=self.user.supplier, author=self.user, active=True)

      groups = Group.objects.filter(active=True, supplierorggroupconn__supplier_org=self.user.supplier.org).order_by('alias').all()
      self.assertEqual(groups[0].alias, 'group_11')
      self.assertEqual(groups[1].alias, 'group_12')
