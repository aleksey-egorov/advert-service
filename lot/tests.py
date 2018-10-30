from django.test import TestCase
from django.utils import timezone
from lot.models import Lot, Currency
from brand.models import Brand
from product.models import Product, Group, Category
from user.models import User
from supplier.models import Supplier
from geo.models import Region

# Lot unit tests

class LotTestCase(TestCase):

    def setUp(self):
        Supplier.objects.create(id=1, name="Поставщик")
        self.user = User.objects.create(username='test', password='test', supplier=Supplier.objects.get(id=1))

        Brand.objects.create(id=1, name="KAMAZ")
        Category.objects.create(id=1, name="Строительная техника", sorting=1)
        category = Category.objects.get(id=1)
        Group.objects.create(id=1, name="Самосвалы", category=category)
        brand = Brand.objects.get(id=1)
        group = Group.objects.get(id=1)
        Product.objects.create(id=1, name="KAMAZ-6520", brand=brand, group=group, alias='kamaz-6520', description='test',
                               pub_date=timezone.now(), active=True, upd_date=timezone.now())
        Currency.objects.create(id=1, name="RUR", course=1)
        Region.objects.create(id=1, name="Москва")


    def test_lots_search(self):
        Lot.objects.create(id=1, num="000001", name="КАМАЗ-6520", product=Product.objects.get(id=1), price=2000000,
                             currency=Currency.objects.get(id=1), supplier=Supplier.objects.get(id=1), active=True )
        lots_list = Lot.objects.make_search({'brand': 1})
        lots = lots_list.all()
        self.assertEqual(lots[0].num, '000001')
        self.assertEqual(lots[0].price, 2000000)

        lots_list = Lot.objects.make_search({'group': 1})
        lots = lots_list.all()
        self.assertEqual(lots[0].num, '000001')
        self.assertEqual(lots[0].price, 2000000)

        lots_list = Lot.objects.make_search({'category': 1})
        lots = lots_list.all()
        self.assertEqual(lots[0].num, '000001')
        self.assertEqual(lots[0].price, 2000000)

    def test_add_lot(self):
        data ={
            'product': 1,
            'currency': 1,
            'region': 1,
            'price': 1000000,
            'main_description': 'test',
            'state': 'new',
            'manuf_year': 2017,
            'image_filenames': '[]'
        }
        Lot.objects.add_lot(data, self.user)
        lots_list = Lot.objects.filter()
        lots = lots_list.all()
        self.assertEqual(lots[0].num, '000001')
        self.assertEqual(lots[0].price, 1000000)

    def test_update_lot(self):
        data = {
            'product': 1,
            'currency': 1,
            'region': 1,
            'price': 1200000,
            'main_description': 'test',
            'state': 'new',
            'manuf_year': 2017,
            'image_filenames': '[]'
        }
        Lot.objects.add_lot(data, self.user)
        lots = Lot.objects.filter(price=1200000).all()
        lot_id = lots[0].id
        lot_num = lots[0].num

        udata = {
            'name': 'КАМАЗ 6522',
            'product': 1,
            'currency': 1,
            'region': 1,
            'active': True,
            'best': False,
            'price': 1500000,
            'main_description': 'test',
            'state': 'new',
            'manuf_year': 2018,
            'image_filenames': '[]'
        }
        res = Lot.objects.update_lot(lot_id, udata)
        lots = Lot.objects.filter(price=1500000).all()
        # print ("UPD={} NUM={}".format(res, lot_num))
        self.assertEqual(lots[0].num, lot_num)
        self.assertEqual(lots[0].price, 1500000)
        self.assertEqual(lots[0].manuf_year, 2018)
