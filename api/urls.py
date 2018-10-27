from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

from api.views import LotListAPIView, LotDetailAPIView, LotSearchAPIView, wrong_url, schema_view

urlpatterns = [
    url(regex=r"^docs/", view=schema_view),
    url(regex=r'^token-auth/', view=obtain_jwt_token),
    url(regex=r"^(?P<version>(v1))/lots/(?P<pk>[0-9]+)/",
        view=LotDetailAPIView.as_view(),
        name="lots-detail"),
    url(regex=r"(?P<version>(v1))/lots/search/?$",
        view=LotSearchAPIView.as_view(),
        name="lots-search"),
    url(regex=r"(?P<version>(v1))/lots/",
        view=LotListAPIView.as_view(),
        name="lots-list"),

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
