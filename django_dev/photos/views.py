from django.views.generic import ListView, DetailView
from .models import Photo, Album


class AlbumLV(ListView):
    model = Album


class AlbumDV(DetailView):
    model = Album


class PhotoDV(DetailView):
    model = Photo