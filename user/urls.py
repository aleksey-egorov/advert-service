from django.conf.urls import url, include

from user.views import (
    ProfileView, LotAddView, LotAddDoneView, LotEditView, LotEditDoneView, LotImageAddView,  LotImageDelView, UserLotsView
)

urlpatterns = [
    url(regex=r"profile/", view=ProfileView.as_view()),
    url(regex=r'lot/add/', view=LotAddView.as_view()),
    url(regex=r"lot/add/done/", view=LotAddDoneView.as_view()),
    url(regex=r"lot/edit/(?P<id>[0-9]+)/", view=LotEditView.as_view()),
    url(regex=r"lot/edit/done/", view=LotEditDoneView.as_view()),
    url(regex=r"lot/image/add/", view=LotImageAddView.as_view()),
    url(regex=r"lot/image/del/", view=LotImageDelView.as_view()),
    url(regex=r"lots/?$", view=UserLotsView.as_view()),
]

