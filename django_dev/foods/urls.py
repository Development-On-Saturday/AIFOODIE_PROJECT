from django.urls import path
from .views import predictImage, ClassifierView, FoodPlaceSearch

app_name = "foods"

urlpatterns = [
    path("photos/create/", ClassifierView.as_view(), name="classifier"),
    path("photos/create/predictImage/", predictImage, name="predictImage"),
    path("place/search/", FoodPlaceSearch, name="FoodPlaceSearch"),
    
]

