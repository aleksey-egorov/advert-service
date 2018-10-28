from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

from api.views import (
    LotListAPIView, LotDetailAPIView, LotSearchAPIView, BrandDetailAPIView, BrandListAPIView, BrandSearchAPIView,
    ProductListAPIView, ProductDetailAPIView, ProductSearchAPIView,
    wrong_url, schema_view
)

urlpatterns = [
    url(regex=r"^docs/", view=schema_view),
    url(regex=r'^token-auth/', view=obtain_jwt_token),

    url(regex=r"^(?P<version>(v1))/lots/(?P<pk>[0-9]+)/",
        view=LotDetailAPIView.as_view(), name="lot-detail"),
    url(regex=r"(?P<version>(v1))/lots/search/?$",
        view=LotSearchAPIView.as_view(), name="lot-search"),
    url(regex=r"(?P<version>(v1))/lots/",
        view=LotListAPIView.as_view(), name="lot-list"),

    url(regex=r"^(?P<version>(v1))/brands/(?P<pk>[0-9]+)/",
        view=BrandDetailAPIView.as_view(), name="brand-detail"),
    url(regex=r"(?P<version>(v1))/brands/search/?$",
        view=BrandSearchAPIView.as_view(), name="brand-search"),
    url(regex=r"(?P<version>(v1))/brands/",
        view=BrandListAPIView.as_view(), name="brand-list"),

    url(regex=r"^(?P<version>(v1))/products/(?P<pk>[0-9]+)/",
        view=ProductDetailAPIView.as_view(), name="product-detail"),
    url(regex=r"(?P<version>(v1))/products/search/?$",
        view=ProductSearchAPIView.as_view(), name="product-search"),
    url(regex=r"(?P<version>(v1))/products/",
        view=ProductListAPIView.as_view(), name="product-list"),

    #url(regex=r"^(?P<version>(v1|v2))/trending/",
    #    view=TrendingAPIView.as_view(),
    #    name="trending"),
    #url(regex=r"^(?P<version>(v1|v2))/search/?$",
    #    view=SearchAPIView.as_view(),
    #    name="search"),
    #url(regex=r"^(?P<version>(v1|v2))/questions/(?P<pk>[0-9]+)/answers/",
    #    view=QuestionAnswersAPIView.as_view(),
    #    name="answer"),

    url(regex=r'^', view=wrong_url),

]
