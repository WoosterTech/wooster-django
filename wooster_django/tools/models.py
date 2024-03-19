# from collections.abc import Iterable
from django.db.models import Max, Model, PositiveSmallIntegerField

from .managers import RankManager


# Create your models here.
class RankedModel(Model):
    class Meta:
        abstract = True

    rank = PositiveSmallIntegerField()

    objects = RankManager()

    def save(self, *args, **kwargs) -> None:
        if self._state.adding:
            results = self.__class__.objects.aggregate(Max("rank"))
            current_max = results["rank__max"]
            return current_max + 1
        return super().save(*args, **kwargs)
