from django.urls import path
from receipts.views import CreateReceiptView, MerchantCreateView, MerchantDetailView, MerchantListView

app_name = "receipts"
# fmt: off
urlpatterns = [
    path("new/", CreateReceiptView.as_view(), name="create_receipt"),
    path("merchant/new/", MerchantCreateView.as_view(), name="create_merchant"),
    path("merchant/<slug:slug>", MerchantDetailView.as_view(), name="detail_merchant"),
    path("merchant/list/", MerchantListView.as_view(), name="list_merchant")
]
