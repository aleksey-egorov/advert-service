from django.contrib.auth.models import User, Group
from rest_framework import serializers

from lot.models import Lot
from brand.models import Brand
from product.models import Product

class LotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lot
        fields = ('id', 'name', 'product_name', 'price', 'currency_name', 'manuf_year', 'state_name')

class LotFullSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lot
        fields = ('id', 'name', 'product_name', 'price', 'currency_name', 'manuf_year', 'state_name', 'main_description',
                  'supplier_name', 'pub_date', 'upd_date', 'main_image', 'region_name', 'new_prod_state', 'best', 'num', 'alias', 'tags_list')

class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'logo')

class BrandFullSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'logo', 'description', 'rating', 'popular', 'alias', 'tags_list')

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'brand_name', 'group_name')

class ProductFullSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'brand_name', 'group_name', 'description', 'pub_date', 'upd_date', 'alias', 'main_image')