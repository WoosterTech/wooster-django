import json

from celery import Celery
from django.conf import settings
from receiptparser.doc_intel_receipt import analyze_receipt
from receipts.models import Receipt

app = Celery("tasks", broker=settings["CELERY_BROKER"])


@app.task
def analyze_receipt_task(receipt_file):
    receipts = analyze_receipt(receipt_file)

    for receipt in receipts:
        _receipt_model = Receipt.objects.create(receipt_file=receipt_file, analyze_result=json.dump(receipt.as_dict()))
