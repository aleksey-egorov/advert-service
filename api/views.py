from django.conf import settings
from django.db.models import Q
from rest_framework.decorators import api_view, schema, renderer_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework import response, schemas

from lot.models import Lot
from brand.models import Brand
from product.models import Product
from api.serializers import (
    LotSerializer, LotFullSerializer, BrandSerializer, BrandFullSerializer, ProductSerializer, ProductFullSerializer
)


class LotListAPIView(generics.ListAPIView):
    queryset = Lot.objects.filter(active=True).order_by('-pub_date').all()
    serializer_class = LotSerializer

class LotDetailAPIView(generics.RetrieveAPIView):
    serializer_class = LotFullSerializer
    lookup_field = 'pk'
    queryset = Lot.objects.filter(active=True).order_by('-pub_date').all()

class LotSearchAPIView(generics.ListAPIView):
    serializer_class = LotSerializer

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Lot.objects.filter(active=True).filter(Q(name__icontains=query)).order_by('-pub_date')
        return queryset


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.filter(active=True).order_by('name').all()
    serializer_class = BrandSerializer

class BrandDetailAPIView(generics.RetrieveAPIView):
    serializer_class = BrandFullSerializer
    lookup_field = 'pk'
    queryset = Brand.objects.filter(active=True).order_by('name').all()

class BrandSearchAPIView(generics.ListAPIView):
    serializer_class = BrandSerializer

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Brand.objects.filter(active=True).filter(Q(name__icontains=query)).order_by('name')
        return queryset


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(active=True).order_by('name').all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductFullSerializer
    lookup_field = 'pk'
    queryset = Product.objects.filter(active=True).order_by('name').all()

class ProductSearchAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Product.objects.filter(active=True).filter(Q(name__icontains=query)).order_by('name')
        return queryset


@api_view()
@schema(None)
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Advert API')
    return response.Response(generator.get_schema(request=request))

@api_view()
@schema(None)
def wrong_url(request):
    return Response({"message": "Wrong URL: check API documentation at http://{}/api/docs/".format(settings.SITE_URL)})
