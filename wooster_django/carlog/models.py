from django.db import models
from django.utils.translation import gettext_lazy as _
from slugify import slugify


# Create your models here.
class BaseModel(models.Model):
    name = models.CharField(_("name"), max_length=50)
    created_datetime = models.DateTimeField(_("created datetime"), auto_now=False, auto_now_add=True)
    modified_datetime = models.DateTimeField(_("modified datetime"), auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class CarMake(BaseModel):
    pass


class Model(BaseModel):
    make = models.ForeignKey(CarMake, verbose_name=_("Make"), on_delete=models.CASCADE)


class Car(BaseModel):
    model = models.ForeignKey(Model, verbose_name=_("Model"), on_delete=models.PROTECT)


class ServiceType(models.Model):
    name = models.CharField(_("Service Name"), max_length=50)


class ServiceLog(models.Model):
    mileage = models.DecimalField(_("Current Milleage"), max_digits=15, decimal_places=2)
    name = None
    service_types = models.ManyToManyField("app.Model", verbose_name=_(""))
