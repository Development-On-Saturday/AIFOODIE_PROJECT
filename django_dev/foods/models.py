from django.db import models
from core.models import TimeStampedModel
from .fields import ThumbnailImageField


# class Photo(TimeStampedModel):

#     """ Photo Model Definition """

#     file = models.ImageField(upload_to="food_photos")
#     food = models.ForeignKey("Food", related_name="photos", on_delete=models.CASCADE)


class Food(TimeStampedModel):

    """ Food Model Definition """

    name = models.CharField(max_length=20)
    user = models.ForeignKey(
        "users.User", related_name="foods", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="food_photos/photo/%Y/%m", blank=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.name
