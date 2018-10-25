from django.conf.urls import url, include

from acomp.views import BrandAcompView, ProductAcompView, RegionListAcompView, SessionAcompView

urlpatterns = [
    url(regex=r"^brand/",
        view=BrandAcompView.as_view()),
    url(regex=r"^product/",
        view=ProductAcompView.as_view()),
    url(regex=r"^region/list/",
        view=RegionListAcompView.as_view()),
    url(regex=r"^session/",
        view=SessionAcompView.as_view())
]
