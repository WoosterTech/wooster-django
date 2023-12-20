from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from slugify import slugify


# Create your models here.
class BaseModel(models.Model):
    """Base model for standardization. Includes generating slug."""

    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("created by"), on_delete=models.PROTECT)
    slug = models.SlugField(unique=True, editable=False)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modified date"), auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DocumentNumber(models.Model):
    document = models.CharField(max_length=50, primary_key=True, unique=True)
    prefix = models.CharField(max_length=10, blank=True, null=True)
    padding_digits = models.IntegerField(blank=True, null=True)
    next_counter = models.IntegerField(default=1)
    last_number = models.CharField(max_length=50, editable=False, null=True)
    last_generated_date = models.DateTimeField(auto_now=True)

    def get_next_number(self):
        prefix = self.prefix
        next_counter = self.next_counter
        padded_counter = str(next_counter).zfill(self.padding_digits)
        number = f"{prefix}{padded_counter}"

        self.next_counter += 1
        self.last_number = number

        self.save()

        return number
