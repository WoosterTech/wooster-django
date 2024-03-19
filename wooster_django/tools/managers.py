from django.db.models import Count, F, Manager, Max, Model
from django.db.transaction import atomic


class InvalidRankError(Exception):
    pass


class RankManager(Manager):
    def move(self, obj: Model, new_rank: int):
        if new_rank < 1:
            raise InvalidRankError("Unable to set rank below '1'; already highest rank.")
        elif new_rank == obj.get_next_rank():
            raise InvalidRankError(f"Unable to set rank above '{obj.rank}'; already lowest rank.")

        qs = self.get_queryset()
        current_rank = obj.rank  # set temp variable for filters below
        # obj.rank = 0
        qs.filter(pk=obj.pk).update(rank=0)  # avoid unique constraint (no values should be zero)

        with atomic():
            if current_rank > int(new_rank):
                qs.filter(
                    parent_model=obj.parent_model,
                    rank__lt=current_rank,
                    rank__gte=new_rank,
                ).exclude(
                    pk=obj.pk,
                ).order_by("-rank").update(
                    rank=F("rank") + 1,
                )
            else:
                qs.filter(
                    parent_model=obj.parent_model,
                    rank__lte=new_rank,
                    rank__gt=current_rank,
                ).exclude(
                    pk=obj.pk,
                ).update(
                    rank=F("rank") - 1,
                )

        obj.rank = new_rank
        obj.save()

    def create(self, **kwargs):
        instance = self.model(**kwargs)

        with atomic():
            instance.rank = instance.get_next_rank()
            instance.save()

            return instance

    def move_to_end(self, obj):
        current_rank = obj.rank

        if (obj.get_next_rank() - 1) == current_rank:
            raise InvalidRankError(f"Unable to move to end; '{current_rank}' already lowest rank.")

        qs = self.get_queryset()

        with atomic():
            qs.filter(pk=obj.pk).update(rank=obj.get_next_rank())

            # if current_rank == obj.rank: raise InvalidRankError("Unable to move to end; '{}'
            #     already lowest rank.".format(current_rank))

            qs.filter(
                parent_model=obj.parent_model,
                rank__gt=current_rank,
            ).order_by(
                "rank"
            ).update(rank=F("rank") - 1)

    def move_to_top(self, obj):
        if obj.rank == 1:
            raise InvalidRankError("Unable to set rank below '1'; already highest rank.")

        current_rank = obj.rank

        qs = self.get_queryset()

        with atomic():
            qs.filter(pk=obj.pk).update(rank=0)

            qs.filter(
                parent_model=obj.parent_model,
                rank__lt=current_rank,
            ).order_by(
                "-rank"
            ).update(rank=F("rank") + 1)

    def normalize_ranks(self) -> None:
        """Make sure ranks start at 1 and increment with no gaps."""
        qs = self.get_queryset()

        with atomic():
            # kwargs = {field: model[0]}
            qsm = qs.order_by("rank")
            result = qsm.aggregate(Max("rank"), Count("rank"))

            if result["rank__max"] == result["rank__count"] or result["rank__count"] == 0:
                return

            for count, s in enumerate(qsm, 1):
                s.rank = count + int(result["rank__max"])
            self.bulk_update(qsm, ["rank"])

            qsm.update(
                rank=F("rank") - int(result["rank__max"]),
            )

        for obj in qsm:
            print(f"Rank[{obj.name}]: {obj.rank}")
