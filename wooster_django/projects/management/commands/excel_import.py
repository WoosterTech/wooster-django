import csv  # noqa: F401
from typing import Any

from customers.models import Customer  # noqa: F401
from django.conf import settings  # noqa: F401
from django.core.management.base import BaseCommand, CommandParser
from projects.models import Project  # noqa: F401


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("csv_file", nargs="+", type=str)

    def handle(self, *args: Any, **options: Any) -> str | None:
        return super().handle(*args, **options)
