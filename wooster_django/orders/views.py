from django.shortcuts import render

from .models import Invoice


# Create your views here.
def printable_invoice(request, slug: str):
    invoice = Invoice.objects.filter(slug=slug).select_related("customer").prefetch_related("invoiceline_set")
    context = {"invoice": invoice.first()}
    return render(request, "orders/invoice.html", context)
