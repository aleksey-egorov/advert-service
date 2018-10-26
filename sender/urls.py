from django.conf.urls import url, include

from sender.views import BrandSendMessageView, SupplierOrgSendMessageView

urlpatterns = [
    url(regex=r"^brand/",
        view=BrandSendMessageView.as_view()),
    url(regex=r"^supplier_org/",
        view=SupplierOrgSendMessageView.as_view())
]
