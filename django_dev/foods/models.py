from django.db import models
from core.models import TimeStampedModel

class Food(TimeStampedModel):

    """ Food Model Definition """

    name = models.CharField(max_length=20)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.name
