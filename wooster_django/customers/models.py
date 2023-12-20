# from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# from slugify import slugify
# from wooster_django.basemodels.models import BaseModel


# Create your models here.
# class BaseModel(models.Model):
#     """Base model for standardization. Includes generating slug."""

#     name = models.CharField(max_length=50)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("created by"), on_delete=models.PROTECT)
#     slug = models.SlugField(unique=True, editable=False)
#     created_date = models.DateTimeField(_("created date"), auto_now_add=True)
#     modified_date = models.DateTimeField(_("modified date"), auto_now=True)

#     class Meta:
#         abstract = True

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)


class Customer(models.Model):
    """Simple customer model"""

    name = None
    organization_name = models.CharField(_("organization name"), max_length=100, unique=True)
    contact_name = models.CharField(_("contact full name"), max_length=100)
    contact_email = models.EmailField(_("contact email"), max_length=254, blank=True)
    contact_phone = PhoneNumberField(_("contact phone number"), blank=True)

    def __str__(self) -> str:
        return self.organization_name
