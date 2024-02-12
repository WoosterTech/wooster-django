from django.contrib.auth import get_user_model

# from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from .models import Receipt

User = get_user_model()


# Create your views here.
class BaseCreateView(CreateView):
    class Meta:
        abstract = True

    pass


class CreateReceiptView(BaseCreateView):
    model = Receipt
    fields = ["receipt_file"]
