from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class ImageModel(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)


class ImageLike(models.Model):
    image = models.ForeignKey(ImageModel, on_delete=models.PROTECT, related_name='image_like')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
