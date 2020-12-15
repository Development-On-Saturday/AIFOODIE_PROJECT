from django.views.generic import ListView, DetailView
from .models import Photo, Album
from users.mixins import LoggedInOnlyView


class AlbumLV(LoggedInOnlyView, ListView):
    model = Album


class AlbumDV(LoggedInOnlyView,DetailView):
    model = Album


class PhotoDV(LoggedInOnlyView,DetailView):
    model = Photo