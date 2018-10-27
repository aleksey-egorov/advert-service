from django.test import TestCase
from django.utils import timezone

from brand.models import Brand
from product.models import Product, Group, Category

# Brand unit tests.

class BrandTestCase(TestCase):

    def setUp(self):
        Brand.objects.create(id=1, name="KAMAZ")
        Brand.objects.create(id=2, name="SCANIA")
        Category.objects.create(id=1, name="Строительная техника", sorting=1, alias='str', active=True)
        Category.objects.create(id=2, name="Дорожная техника", sorting=1, alias='dor', active=True)
        category = Category.objects.get(id=1)
        category2 = Category.objects.get(id=2)
        Group.objects.create(id=1, name="Самосвалы", category=category, active=True, alias='group_1')
        Group.objects.create(id=2, name="Грузовые автомобили", category=category2, active=True, alias='group_2')

    def test_brandgroup_conn(self):
        brand = Brand.objects.get(id=1)
        group = Group.objects.get(id=1)
        group2 = Group.objects.get(id=2)
        Product.objects.create(id=1, name="KAMAZ-6521", brand=brand, group=group,
                               alias='kamaz-6521', description='test',
                               pub_date=timezone.now(), active=True, upd_date=timezone.now())
        Product.objects.create(id=2, name="KAMAZ-6522", brand=brand, group=group2,
                               alias='kamaz-6522', description='test',
                               pub_date=timezone.now(), active=True, upd_date=timezone.now())
        groups = Group.objects.filter(active=True, brandgroupconn__brand=brand).order_by('alias').all()
        self.assertEqual(groups[0].alias, 'group_1')
        self.assertEqual(groups[1].alias, 'group_2')

    def test_brandcategory_conn(self):
        brand = Brand.objects.get(id=1)
        group = Group.objects.get(id=1)
        group2 = Group.objects.get(id=2)
        Product.objects.create(id=1, name="KAMAZ-6521", brand=brand, group=group,
                               alias='kamaz-6521', description='test',
                               pub_date=timezone.now(), active=True, upd_date=timezone.now())
        Product.objects.create(id=2, name="KAMAZ-6522", brand=brand, group=group2,
                               alias='kamaz-6522', description='test',
                               pub_date=timezone.now(), active=True, upd_date=timezone.now())
        categories = Category.objects.filter(active=True, brandcategoryconn__brand=brand).order_by('alias').all()
        self.assertEqual(categories[0].alias, 'dor')
        self.assertEqual(categories[1].alias, 'str')
