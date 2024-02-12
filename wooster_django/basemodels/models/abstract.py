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
