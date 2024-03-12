# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
from django.forms import FileField, Form
from receipts.functions import allowed_file

# from receipts.models import Receipt  # , Merchant


# class ReceiptCreateForm(forms.Form):
#     upload_receipt = forms.FileField()

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_id = "id-receiptUploadForm"
#         self.helper.form_class = "uploadForms"
#         self.helper.form_method = "post"
#         self.helper.form_action = "upload_receipt"

#         self.helper.add_input(Submit("submit", "Submit"))


# class MerchangeCreateForm(ModelForm):
#     class Meta:
#         model = Merchant


# class ReceiptUploadForm(ModelForm):
#     class Meta:
#         model = Receipt
#         fields = ("receipt_file",)


class ReceiptUploadForm(Form):
    receipt_file = FileField()

    def is_valid(self) -> bool:
        validity = super().is_valid()
        validity = allowed_file(self.files["file"]) if validity else validity

        return validity
