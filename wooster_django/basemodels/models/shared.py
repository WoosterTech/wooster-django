from django.db import models


# Create your models here.
class WhyDoesThisError(models.Model):
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
