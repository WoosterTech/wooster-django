from datetime import date

# from django.http import HttpResponseRedirect
# from django.shortcuts import render
from pathlib import Path

from django.contrib.auth import get_user_model
from django.urls import reverse

# from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView
from receipts.forms import ReceiptUploadForm
from receipts.models import Merchant, Receipt
from shortuuid import uuid

# from receiptparser.doc_intel_receipt import analyze_receipt

User = get_user_model()


# Create your views here.
class BaseCreateView(CreateView):
    class Meta:
        abstract = True

    pass


class BaseDetailView(DetailView):
    class Meta:
        abstract = True

    pass


class BaseListView(ListView):
    class Meta:
        abstract = True

    pass


class MerchantCreateView(BaseCreateView):
    model = Merchant
    fields = ["name", "created_by"]


class MerchantDetailView(BaseDetailView):
    model = Merchant


class MerchantListView(BaseListView):
    model = Merchant


class CreateReceiptView(BaseCreateView):
    model = Receipt
    fields = ["receipt_file"]
    form = ReceiptUploadForm


def upload_receipt(request):
    if request.method == "POST":
        form = ReceiptUploadForm(request.Post, request.Files)
        if form.is_valid():
            _receipt = handle_uploaded_file(request.FILES["file"])
            return reverse("receipts:upload")


def handle_uploaded_file(file) -> Receipt:
    extension = Path(file).suffix

    new_filename = uuid()
    today = date.today()
    year = today.strftime("/%Y")
    month = today.strftime("/%m")

    new_path = f"uploads/{year}/{month}/{new_filename}{extension}"

    with open(new_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    new_receipt = Receipt.objects.create(receipt_file=new_path)

    return new_receipt


# def upload_file(request):
#     if request.method == "POST":
#         form = ReceiptUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/receipts/new/")
#     else:
#         form = ReceiptUploadForm()

#     return render(request, "receipt_form.html", {"form", form})
