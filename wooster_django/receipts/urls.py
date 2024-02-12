from django.urls import path

from .views import CreateReceiptView

app_name = "receipts"
# fmt: off
urlpatterns = [
    path("create-receipt/", CreateReceiptView.as_view(), name="create_receipt")
]
