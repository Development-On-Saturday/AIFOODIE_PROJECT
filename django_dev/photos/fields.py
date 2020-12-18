import os 
from PIL import Image
from django.db.models.fields.files import ImageField, ImageFieldFile

class ThumbnailImageFieldFile(ImageFieldFile):
    def _add_thumb(self, s):
        parts = s.split(".")
        parts.insert(-1, "thumb")
        if parts[-1].lower() not in ["jpeg",'jpg']:
            parts[-1] = "jpg"
        return ".".join(parts)

    @property
    def thumb_path(self):
        return self._add_thumb(self.path)
    
    @property
    def thumb_url(self):
        return self._add_thumb(self.url)

    def save(self, name, content, save=True):
        super().save(name, content, save)

        img = Image.open(self.path)
        size = (self.field.thumb_width, self.field.thumb_height)
        img.thumbnail(size)
        background = Image.new("RGB", size, (255,255,255))
        box = (int((size[0] - img.size[0]) / 2), int((size[1] - img.size[1]) / 2))
        background.paste(img, box)
        background.save(self.thumb_path,"JPEG")

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super().delete(save)

class ThumbnailImageField(ImageField):
    attr_class = ThumbnailImageFieldFile

    def __init__(self, verbose_name = None, thumb_width=128, thumb_height=128, **kwargs):
        self.thumb_width, self.thumb_height = thumb_width, thumb_height
        super().__init__(verbose_name, **kwargs)