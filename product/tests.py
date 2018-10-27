from django.test import TestCase
from django.utils import timezone

from brand.models import Brand
from product.models import Product, Group, Category

# Product unit tests.

class ProductTestCase(TestCase):

    def setUp(self):
        Brand.objects.create(id=1, name="KAMAZ")
        Category.objects.create(id=1, name="Строительная техника", sorting=1, alias='str', active=True)
        Category.objects.create(id=2, name="Карьерная техника", sorting=1, alias='dor', active=True)
        category1 = Category.objects.get(id=1)
        category2 = Category.objects.get(id=2)
        Group.objects.create(id=1, name="Самосвалы строительные", category=category1, active=True, alias='group_1')
        Group.objects.create(id=2, name="Самосвалы карьерные", category=category2, active=True, alias='group_2')
        Group.objects.create(id=3, name="Самосвалы (двухосные)", active=True, alias='group_3')

    def test_group_categories(self):
        group1 = Group.objects.get(id=1)
        group2 = Group.objects.get(id=2)
        group3 = Group.objects.get(id=3)
        group3.parents.add(group1)
        group3.parents.add(group2)
        categories = group3.get_categories()
        self.assertEqual(categories, [1,2])

    def test_group_url(self):
        group1 = Group.objects.get(id=1)
        group2 = Group.objects.get(id=2)
        group3 = Group.objects.get(id=3)
        group3.parents.add(group1)
        self.assertEqual(group3.get_url(), 'group_1/group_3/')
        self.assertEqual(group2.get_url(), 'group_2/')

    def test_category_has_products(self):
        group1 = Group.objects.get(id=1)
        brand = Brand.objects.get(id=1)
        category1 = Category.objects.get(id=1)
        Product.objects.create(id=1, name="KAMAZ-6520", brand=brand, group=group1, alias='kamaz-6520',
                               description='test', pub_date=timezone.now(), active=True, upd_date=timezone.now())
        has = category1.has_products(brand)
        self.assertEqual(has, True)