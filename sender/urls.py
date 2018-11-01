from django.conf.urls import url, include

from sender.views import  (
    BrandSendMessageView, SupplierOrgSendMessageView, SupplierSendMessageView, LotCreditMessageView,
    LotLeasingMessageView, LotRentMessageView
)

urlpatterns = [
    url(regex=r"^brand/",
        view=BrandSendMessageView.as_view()),
    url(regex=r"^supplier_org/",
        view=SupplierOrgSendMessageView.as_view()),
    url(regex=r"^supplier/",
        view=SupplierSendMessageView.as_view()),
    url(regex=r"^credit/",
        view=LotCreditMessageView.as_view()),
    url(regex=r"^leasing/",
        view=LotLeasingMessageView.as_view()),
    url(regex=r"^rent/",
        view=LotRentMessageView.as_view()),
]
