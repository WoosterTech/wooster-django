from django.urls import path

from .views import printable_invoice

app_name = "orders"
# fmt: off
urlpatterns = [
    path("invoices/<str:slug>/printable", printable_invoice, name="invoice_detail_printable"),
]
