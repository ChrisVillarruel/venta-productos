from django.db import models
from django.contrib.auth.models import AbstractUser
from config.settings import MEDIA_URL, STATIC_URL

# Create your models here.


class User(AbstractUser):
    image = models.ImageField(verbose_name='Foto de perfil', upload_to='users/%Y/%m/%d', null=True, blank=True)

    def get_image(self):
        if self.image:
            return f'{MEDIA_URL}{self.image}'
        return f'{STATIC_URL}{"img/userDefault.png"}'
