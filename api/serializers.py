from django.contrib.auth.models import User, Group
from rest_framework import serializers

from lot.models import Lot

class LotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lot
        fields = ('id', 'name', 'product_name', 'price', 'currency_name', 'manuf_year', 'state_name')

class LotFullSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lot
        fields = ('id', 'name', 'product_name', 'price', 'currency_name', 'manuf_year', 'state_name', 'main_description',
                  'supplier_name', 'pub_date', 'upd_date', 'main_image', 'region_name', 'new_prod_state', 'best', 'num')


