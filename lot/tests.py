import datetime
from django.test import TestCase

from lot.models import Lot
from brand.models import Brand
from product.models import Product, Group, Category
from user.models import User

# Create your tests here.


class LotTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', password='test')
        Brand.objects.create(id=1, name="KAMAZ")
        Category.objects.create(id=1, name="Строительная техника", sorting=1)
        category = Category.objects.get(id=1)
        Group.objects.create(id=1, name="Самосвалы", category=category)
        brand = Brand.objects.get(id=1)
        group = Group.objects.get(id=1)
        Product.objects.create(id=1, name="KAMAZ-6520", brand=brand, group=group, alias='kamaz-6520', description='test',
                               pub_date=datetime.datetime.now(), upd_date=datetime.datetime.now())
        Lot.objects.create(id=1, num="000001", name="КАМАЗ-6520", product=Product.objects.get(id=1), active=True )


    def test_lots_search(self):
        """"""
        lots_list = Lot.objects.make_search({'brand': 1})
        lots = lots_list.all()
        self.assertEqual(lots[0].num, '000001')

        lots_list = Lot.objects.make_search({'group': 1})
        lots = lots_list.all()
        self.assertEqual(lots[0].num, '000001')

        lots_list = Lot.objects.make_search({'category': 1})
        lots = lots_list.all()
        self.assertEqual(lots[0].num, '000001')