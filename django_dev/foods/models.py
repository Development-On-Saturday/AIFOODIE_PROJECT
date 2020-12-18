from django.db import models
from core.models import TimeStampedModel

class Food(TimeStampedModel):

    """ Food Model Definition """

    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to="foods/%Y/%m/%d", blank=True)
    user = models.ForeignKey("users.User", related_name="foods", on_delete=models.CASCADE, null=True)
    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.name
