from django.conf.urls import url, include

from sender.views import BrandSendMessageView

urlpatterns = [
    url(regex=r"^brand/",
        view=BrandSendMessageView.as_view())
]
